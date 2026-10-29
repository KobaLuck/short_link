from flask import render_template, redirect, flash, request, Blueprint
from yacut import db
from yacut.models import URLMap
from yacut.forms import URLForm
from yacut.utils import get_unique_short_id
from dotenv import load_dotenv
from yacut.forms import FileUploadForm
import os
import urllib.parse
import asyncio
import aiohttp

load_dotenv()


bp = Blueprint('main', __name__)

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_TOKEN = os.getenv('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'} if DISK_TOKEN else {}


@bp.route('/', methods=['GET', 'POST'])
def index_view():
        form = URLForm()
        if form.validate_on_submit():
            original_link = form.original_link.data
            custom_id = form.custom_id.data or get_unique_short_id()

            # block reserved and invalid ids
            if len(custom_id) > 16 or not custom_id.isalnum() or custom_id == 'files':
                return render_template('index.html', form=form)

            if URLMap.query.filter_by(short=custom_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)

            new_link = URLMap(original=original_link, short=custom_id)
            db.session.add(new_link)
            db.session.commit()

            flash(f'Ссылка создана: {request.host_url}{custom_id}', 'success')
            return render_template('index.html', form=form, short_link=custom_id)

        return render_template('index.html', form=form)


@bp.route('/<string:short_id>')
def redirect_view(short_id):
        url_map = URLMap.query.filter_by(short=short_id).first_or_404()
        return redirect(url_map.original)


@bp.route('/files', methods=['GET', 'POST'])
def files_view():
        form = FileUploadForm()
        file_links = []

        if request.method == 'POST' and form.validate_on_submit():
            if not DISK_TOKEN:
                flash('Токен Яндекс.Диска не найден. Добавьте его в .env как DISK_TOKEN.', 'error')
                return render_template('files.html', form=form)

            files = request.files.getlist('files')
            if not files:
                flash('Выберите хотя бы один файл.', 'error')
                return render_template('files.html', form=form)

            async def upload_and_get_link(session, storage_file):
                filename = storage_file.filename
                if not filename:
                    return None
                params = {'path': f'app:/{filename}', 'overwrite': 'true'}
                async with session.get(UPLOAD_URL, headers=AUTH_HEADERS, params=params) as resp:
                    if resp.status >= 400:
                        return None
                    data = await resp.json()
                    upload_url = data.get('href')
                if not upload_url:
                    return None
                # Reset pointer for reading
                storage_file.stream.seek(0)
                async with session.put(upload_url, data=storage_file.stream) as put_resp:
                    if put_resp.status >= 400:
                        return None
                    location = put_resp.headers.get('Location', '')
                    location = urllib.parse.unquote(location).replace('/disk', '')
                async with session.get(DOWNLOAD_URL, headers=AUTH_HEADERS, params={'path': location}) as dl_resp:
                    if dl_resp.status >= 400:
                        return None
                    dl_data = await dl_resp.json()
                    download_link = dl_data.get('href')
                return (filename, download_link)

            async def process_files_async(file_list):
                connector = aiohttp.TCPConnector()
                async with aiohttp.ClientSession(connector=connector) as session:
                    tasks = [upload_and_get_link(session, f) for f in file_list]
                    return await asyncio.gather(*tasks)

            results = asyncio.run(process_files_async(files))
            for result in results:
                if result and result[1]:
                    file_links.append(result)

            if file_links:
                flash('Файлы успешно загружены на Яндекс.Диск!', 'success')

        return render_template('files.html', form=form, file_links=file_links)


import re
from flask import jsonify, request, Blueprint
from yacut import db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


bp = Blueprint('api', __name__, url_prefix='/api')
_ALNUM_RE = re.compile(r'^[A-Za-z0-9]+$')


def _make_short_link(host_url: str, short_id: str) -> str:
    return f'{host_url.rstrip("/")}/{short_id}'


@bp.route('/id/', methods=['POST'])
def create_id():
    if not request.is_json:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400
    if not isinstance(data, dict):
        return jsonify({'message': 'Тело запроса должно быть объектом JSON'}), 400
    if 'url' not in data:
        return jsonify({'message': '"url" является обязательным полем!'}), 400

    original_url = data.get('url')
    custom_id = data.get('custom_id')

    if not isinstance(original_url, str) or not original_url.strip() or len(original_url) > 2048:
        return jsonify({'message': 'Указана недопустимая исходная ссылка'}), 400
    if custom_id is not None and not isinstance(custom_id, str):
        return jsonify({'message': 'Указано недопустимое имя для короткой ссылки'}), 400

    if custom_id:
        if len(custom_id) > 16 or not _ALNUM_RE.fullmatch(custom_id) or custom_id == 'files':
            return jsonify({'message': 'Указано недопустимое имя для короткой ссылки'}), 400
        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify({'message': 'Предложенный вариант короткой ссылки уже существует.'}), 400
        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = URLMap(original=original_url, short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': original_url,
        'short_link': _make_short_link(request.host_url, short_id),
    }), 201


@bp.route('/id/<string:short_id>/', methods=['GET'])
def get_original(short_id: str):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200


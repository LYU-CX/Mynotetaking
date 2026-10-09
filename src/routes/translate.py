from flask import Blueprint, current_app, jsonify, request
from openai import OpenAIError

from translator import llm_generate

translate_bp = Blueprint('translate', __name__)

SUPPORTED_LANGUAGES = {
    'Chinese',
    'English',
    'Japanese',
    'Korean',
    'Spanish',
    'French',
    'German',
}


@translate_bp.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON request body is required'}), 400

    text = data.get('text')
    target_language = data.get('target_language')
    if not isinstance(text, str) or not text.strip():
        return jsonify({'error': 'Text is required'}), 400
    if not isinstance(target_language, str) or target_language not in SUPPORTED_LANGUAGES:
        return jsonify({'error': 'A supported target_language is required'}), 400

    try:
        translation = llm_generate(text, target_language)
    except (OpenAIError, OSError, ValueError):
        current_app.logger.exception('Translation request failed')
        return jsonify({'error': 'Translation service is unavailable'}), 502

    if not isinstance(translation, str) or not translation.strip():
        current_app.logger.error('Translation service returned an empty result')
        return jsonify({'error': 'Translation service returned no result'}), 502

    return jsonify({'translation': translation})

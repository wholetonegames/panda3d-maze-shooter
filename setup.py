from setuptools import setup

setup(
    name="maze_shooter",
    options = {
        'build_apps': {
            'platforms': [
                'win_amd64',
                'win32',
             ],
            'include_patterns': [
                '**/*.ogg',
                '**/*.wav',
                '**/*.egg'
            ],
            'exclude_patterns': [
                '**/*.txt',
                '**/*.png',
                '**/*.jpg',
            ],
            'gui_apps': {
                'maze_shooter': 'game.py',
            },
            'log_filename': 'output.log',
            'log_append': True,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)

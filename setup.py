from setuptools import setup

setup(
    name='OurTWGame',
    options={
        'build_apps': {
            # Build OurTWG.exe as a GUI application
            'gui_apps': {
                'OurTWGame': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': '$USER_APPDATA/OurTWG/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                'egg-models/**/*.png',
                'egg-models/**/*.jpg',
                'egg-models/**/*.egg',
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
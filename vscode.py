import dotbot
import subprocess

class VSCode(dotbot.Plugin):
    directive = 'vscode'
    installed_extensions = None

    def __init__(self, context):
        super(VSCode, self).__init__(self)

    def can_handle(self, directive):
        return directive == self.directive

    def handle(self, directive, data):
        self.get_installed_extensions()

        status = True
        already_installed = 0

        self._log.info('Installing Visual Studio Code extensions...')

        for item in data:
            if item in self.installed_extensions:
                already_installed = already_installed + 1
                continue

            status = self.install(item)

        if status:
            self._log.info('All extensions installed successfully')
        else:
            self._log.warning('Some extensions have failed to install')

        self._log.info('{} extensions were already installed'.format(
            already_installed
        ))

        return status


    def get_installed_extensions(self):
        """
        Retrieves currently installed Code extensions by running
        `code --list-extensions`.
        """
        process = subprocess.Popen(
            'code --list-extensions --log off',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        return_code = process.wait()

        if return_code == 0:
            out = process.stdout.read().decode()
            self.installed_extensions = out.split('\n')
        else:
            self._log.error(
                'Failed to retrieve currently installed extensions!'
            )


    def install(self, extension):
        self._log.info('Installing extension {}'.format(extension))
        command = 'code --install-extension {}'.format(extension)

        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        return_code = process.wait()

        if return_code != 0:
            self._log.warning('Failed to install {}'.format(extension))
            return False

        return True

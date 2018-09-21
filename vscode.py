import dotbot
import subprocess

class VSCode(dotbot.Plugin):
    directive = 'vscode'

    def __init__(self, context):
        super(VSCode, self).__init__(self)

    def can_handle(self, directive):
        return directive == self.directive

    def handle(self, directive, data):
        status = True

        for item in data:
            status = self.install(item)

        if status:
            self._log.info('All extensions installed successfully')
        else:
            self._log.warning('Some extensions have failed to install')

        return status

    def install(self, extension):
        self._log.info('Installing extension {}'.format(extension))
        command = 'code --install-extension {}'.format(extension)

        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        return_code = process.wait()
        out = process.stdout.read()

        if return_code != 0:
            self._log.warning('Failed to install {}'.format(extension))
            return False

        if 'is already installed' in out.decode():
            self._log.info(
                'Extension {} is already installed'.format(extension)
            )

        return True

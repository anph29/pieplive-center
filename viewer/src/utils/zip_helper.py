import zipfile
import os


def makeZip(directory, targetName):
    with zipfile.ZipFile(f'{directory}\\{targetName}', 'w') as fantasy_zip:
        for folder, subfolders, files in os.walk(directory):
            for file in files:
                fantasy_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file),
                                                  directory), compress_type=zipfile.ZIP_DEFLATED)


def extractZip(zipPath, directory):
    with zipfile.ZipFile(zipPath, 'r') as fantasy_zip:
        fantasy_zip.extractall(directory)


def getAbsPath(path):
    return os.path.dirname(os.path.abspath(path))


if __name__ == "__main__":
    extractZip(getAbsPath('../resource')+'/resource.zip',
               "D:\\anph\\python\\PiepLive-Center\\resourcezip")

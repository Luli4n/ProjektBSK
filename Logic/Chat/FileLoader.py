import os
from pathlib import Path
import tqdm

from Logic.Chat.Frame import Frame, FrameType

BUFFER_SIZE = 65536


class FileLoader:
    def __init__(self, chatWindow):
        self.chatWindow = chatWindow

    def SendFile(self, path, client, encryption_mode):
        filesize = os.path.getsize(path)
        filename=Path(path).stem
        extension = Path(path).suffix

        self.progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B",bar_format='{l_bar}{bar:20}|', unit_scale=True, unit_divisor=1024, ascii=True)

        with open(path, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                client.Send(Frame(bytes_read,FrameType.FILE,file_name=filename,file_extension=extension,encrypt_type=encryption_mode))

                self.progress.update(len(bytes_read))
                self.chatWindow.UpdateBar(self.progress)

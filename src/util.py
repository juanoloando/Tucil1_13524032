import os

def namaFileOutput(directory, namaFile, tipeFile):
    fileOutput = os.path.join(directory, f"{namaFile}.{tipeFile}")
    if not os.path.exists(fileOutput):
        return fileOutput
    counter = 1
    while True:
        fileOutput = os.path.join(directory, f"{namaFile}_{counter}.{tipeFile}")
        if not os.path.exists(fileOutput):
            return fileOutput
        counter += 1

def saveAsTxt(grid, solusi, saveDir="."):
    if not grid:
        return None
    os.makedirs(saveDir, exist_ok=True)
    
    n = len(grid)
    output = [row[:] for row in grid]
    posisiQueen = set(solusi)
    
    for r in range(n):
        for c in range(n):
            if (r, c) in posisiQueen:
                output[r][c] = "#"

    result = "\n".join("".join(row) for row in output)
    filepath = namaFileOutput(saveDir, "Solusi-Queens", "txt")
    
    with open(filepath, "w") as f:
        f.write(result)
    
    return filepath

def saveAsImage(widget, saveDir="."):
    try:
        from PIL import ImageGrab
        os.makedirs(saveDir, exist_ok=True)
        widget.update_idletasks()

        x = widget.winfo_rootx()
        y = widget.winfo_rooty()
        w = x + widget.winfo_width()
        h = y + widget.winfo_height()

        img = ImageGrab.grab((x, y, w, h))
        filepath = namaFileOutput(saveDir, "Solusi-Queens", "png")
        img.save(filepath)
        return True, filepath
    except ImportError:
        return False, "Pillow belum diinstall. Silakan jalankan: pip install Pillow"
    except Exception as e:
        return False, str(e)
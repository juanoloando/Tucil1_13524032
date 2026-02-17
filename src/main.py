import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import sys
import os

_SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_SRC_DIR)
_TEST_DIR = os.path.join(_ROOT_DIR, "test")
os.makedirs(_TEST_DIR, exist_ok=True)

if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from validasiGrid import validasiGrid
from bruteforce import QueensSolution
from util import saveAsTxt, saveAsImage

BG_TOP     = "#e8d5f0"
BG_BOT     = "#f5c6d0"
SIDEBAR_BG = "#dfc8d8"
BTN_BG     = "#ddc8d2"
BTN_HOVER  = "#cbb5bf"
BTN_FG     = "#2a2a2a"

FONT_BTN  = ("Georgia", 11)
FONT_INFO = ("Georgia", 14, "bold")

PALETTE = [
    "#FF9999", "#FFFF99", "#99CCFF", "#99FF99",
    "#FFB366", "#CC99FF", "#C0C0C0", "#FFB3E6",
    "#80FFD4", "#FFD4B3", "#AED6F1", "#A9DFBF",
    "#F9E79F", "#D7BDE2", "#F0B27A", "#85C1E9",
    "#82E0AA", "#F7DC6F", "#BB8FCE", "#EB984E",
    "#FFCCE5", "#B3D9FF", "#CCFFCC", "#FFCC99",
    "#E6CCFF", "#FFE6CC",
]

def warnaBG(parent, w, h, c1, c2):
    cv = tk.Canvas(parent, width=w, height=h, highlightthickness=0, bd=0)
    r1, g1, b1 = parent.winfo_rgb(c1)
    r2, g2, b2 = parent.winfo_rgb(c2)
    for i in range(h):
        t = i / h
        r = int(r1 + (r2 - r1) * t) >> 8
        g = int(g1 + (g2 - g1) * t) >> 8
        b = int(b1 + (b2 - b1) * t) >> 8
        cv.create_line(0, i, w, i, fill=f"#{r:02x}{g:02x}{b:02x}")
    return cv

def atributButton(parent, text, command, bg=BTN_BG, hover=BTN_HOVER, fg=BTN_FG,
                font=FONT_BTN, padx=18, pady=12, wraplength=0):
    kw = dict(text=text, bg=bg, fg=fg, font=font,
              cursor="hand2", relief="flat", padx=padx, pady=pady)
    if wraplength:
        kw["wraplength"] = wraplength
    btn = tk.Label(parent, **kw)
    btn.bind("<Enter>",    lambda e: btn.config(bg=hover))
    btn.bind("<Leave>",    lambda e: btn.config(bg=bg))
    btn.bind("<Button-1>", lambda e: command())
    return btn

class QueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Permainan Queens")
        self.root.resizable(False, False)

        self.grid_data      = []
        self.solusi         = []
        self._solver_thread = None
        self._solving       = False
        self._timer_job     = None
        self._solve_start   = None

        self.homePage()

    def homePage(self):
        self.clear()
        W, H = 900, 600
        self.root.geometry(f"{W}x{H}")

        cv = warnaBG(self.root, W, H, BG_TOP, BG_BOT)
        cv.place(x=0, y=0)

        cv.create_text(W // 2, H // 2 - 100,
                       text="SELAMAT DATANG DI\nQUEENS GAME",
                       font=("Georgia", 36, "bold"),
                       fill="#1a1a1a", justify="center")

        btn_frame = tk.Frame(self.root, bg=BG_TOP)
        btn_frame.place(x=W // 2 - 240, y=H // 2 - 35, width=480, height=70)

        atributButton(btn_frame, "Insert File Test Case (.txt)",
                    command=self.loadFile,
                    padx=20, pady=14).pack(side="left", padx=16)

        atributButton(btn_frame, "Generate Solution",
                    command=self.mulaiSolving,
                    padx=20, pady=14).pack(side="left", padx=16)

    def loadFile(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line]
            self.grid_data = [list(line) for line in lines]
            n = len(self.grid_data)
            messagebox.showinfo("Berhasil", f"File berhasil dimuat!\nGrid: {n} x {n}")
        except Exception as exc:
            messagebox.showerror("Error", f"Gagal membaca file:\n{exc}")

    def mulaiSolving(self):
        if self._solving:
            messagebox.showwarning("Proses penyelesaian", "Solver sedang berjalan!")
            return
        if not self.grid_data:
            messagebox.showerror("Error", "Masukkan file terlebih dahulu!")
            return
        valid, msg = validasiGrid(self.grid_data)
        if not valid:
            messagebox.showerror("Error Validasi", msg)
            return

        self.solusi = []
        self.build_game()
        self._solving     = True
        self._solve_start = time.perf_counter()
        self._start_live_timer()

        self._solver_thread = threading.Thread(target=self.run_solver, daemon=True)
        self._solver_thread.start()

    def _start_live_timer(self):
        self._tick_timer()

    def _tick_timer(self):
        if not self._solving:
            return
        if not hasattr(self, "_time_id"):
            return

        elapsed_ms = int((time.perf_counter() - self._solve_start) * 1000)
        self._bg_cv.itemconfig(self._time_id, text=f"Waktu: {elapsed_ms:,} ms")
        self._timer_job = self.root.after(100, self._tick_timer)

    def _stop_live_timer(self):
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

    def build_game(self):
        self.clear()
        W, H = 1100, 820
        self.root.geometry(f"{W}x{H}")

        self._bg_cv = warnaBG(self.root, W, H, BG_TOP, BG_BOT)
        self._bg_cv.place(x=0, y=0)

        self._bg_cv.create_text(W // 2, 46, text="QUEENS GAME",
                                font=("Georgia", 34, "bold"), fill="#1a1a1a")

        self._subtitle_id = self._bg_cv.create_text(
            W // 2, 88, text="Mencari solusi...",
            font=("Georgia", 16, "bold"), fill="#1a1a1a"
        )

        sidebar = tk.Frame(self.root, bg=SIDEBAR_BG)
        sidebar.place(x=28, y=130, width=230, height=360)

        sidebar_items = [
            ("Insert File Test Case (.txt)", self.loadFile_from_game),
            ("Generate Solution",            self.remulaiSolving),
            ("Save as Image",               self._save_image),
            ("Save as .txt",               self._save_txt),
        ]
        for label, cmd in sidebar_items:
            atributButton(sidebar, label, cmd, padx=10, pady=10,
                        wraplength=200).pack(fill="x", padx=10, pady=8)

        self.n      = len(self.grid_data)
        cell_size   = min(56, max(28, 560 // self.n))
        board_pixel = self.n * cell_size
        board_x     = (W - board_pixel) // 2
        board_y     = 115

        self.board_frame = tk.Frame(self.root, bd=3, relief="solid", bg="#5a90c0")
        self.board_frame.place(x=board_x, y=board_y)

        unique       = sorted(set(c for row in self.grid_data for c in row))
        self._colors = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(unique)}

        self.cells = []
        for r in range(self.n):
            row_cells = []
            for c in range(self.n):
                lbl = tk.Label(
                    self.board_frame, width=2, height=1,
                    bg=self._colors[self.grid_data[r][c]],
                    font=("Segoe UI Emoji", max(9, cell_size // 4)),
                    relief="ridge", bd=1
                )
                lbl.grid(row=r, column=c, padx=1, pady=1,
                         ipadx=max(2, cell_size // 8),
                         ipady=max(2, cell_size // 8))
                row_cells.append(lbl)
            self.cells.append(row_cells)

        info_x = board_x + board_pixel + 45
        self._iter_id = self._bg_cv.create_text(
            info_x, 240, anchor="w", text="Iterasi: 0",
            font=FONT_INFO, fill="#1a1a1a"
        )
        self._time_id = self._bg_cv.create_text(
            info_x, 280, anchor="w", text="Waktu: 0 ms",
            font=FONT_INFO, fill="#1a1a1a"
        )

    def update_ui(self, queens, iteration):
        if not hasattr(self, "cells"):
            return
        snapshot  = list(queens)
        snap_iter = iteration

        def _do():
            if not hasattr(self, "cells"):
                return
            for r in range(self.n):
                for c in range(self.n):
                    self.cells[r][c].config(text="")
            for r, c in snapshot:
                if 0 <= r < self.n and 0 <= c < self.n:
                    self.cells[r][c].config(text="\U0001f451")
            self._bg_cv.itemconfig(self._iter_id, text=f"Iterasi: {snap_iter:,}")
            self.root.update_idletasks()

        self.root.after(0, _do)

    def run_solver(self):
        solver = QueensSolution(self.grid_data, self.update_ui)
        found, solusi, iterasi, waktu = solver.solve()
        self.solusi = solusi
        self._solving = False

        def _done():
            self._stop_live_timer()
            if not hasattr(self, "_bg_cv"):
                return
            if found:
                self.update_ui(solusi, iterasi)
                self._bg_cv.itemconfig(self._subtitle_id, text="Solusi Ditemukan!")
            else:
                if hasattr(self, "cells"):
                    for r in range(self.n):
                        for c in range(self.n):
                            self.cells[r][c].config(text="")
                self._bg_cv.itemconfig(self._subtitle_id, text="Tidak Ada Solusi")

            self._bg_cv.itemconfig(self._iter_id, text=f"Iterasi: {iterasi:,}")
            self._bg_cv.itemconfig(self._time_id, text=f"Waktu: {waktu:,} ms")

        self.root.after(0, _done)

    def loadFile_from_game(self):
        if self._solving:
            messagebox.showwarning("Proses sedang berjalan", "Tunggu solver selesai.")
            return
        self.loadFile()

    def remulaiSolving(self):
        if self._solving:
            messagebox.showwarning("Sedang proses", "Solver sedang berjalan!")
            return
        if not self.grid_data:
            messagebox.showerror("Error", "Masukkan file terlebih dahulu!")
            return
        self.mulaiSolving()

    def _save_image(self):
        if not hasattr(self, "board_frame"):
            messagebox.showerror("Error", "Tidak ada papan untuk disimpan!")
            return
        ok, msg = saveAsImage(self.board_frame, saveDir=_TEST_DIR)
        if ok:
            messagebox.showinfo("Tersimpan", f"Disimpan sebagai {msg}")
        else:
            messagebox.showerror("Error", f"Gagal menyimpan gambar:\n{msg}\n\nJalankan: pip install Pillow")

    def _save_txt(self):
        if not self.solusi:
            messagebox.showerror("Error", "Belum ada solusi untuk disimpan!")
            return
        try:
            filename = saveAsTxt(self.grid_data, self.solusi, saveDir=_TEST_DIR)
            messagebox.showinfo("Tersimpan", f"Disimpan sebagai {filename}\nPosisi queen ditandai dengan '#'.")
        except Exception as exc:
            messagebox.showerror("Error", f"Gagal menyimpan:\n{exc}")

    def clear(self):
        self._stop_live_timer()
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app  = QueensGUI(root)
    root.mainloop()
import time

# Fungsi untuk menentukan iterasi live update brute force
def liveUpdate(n):
    if (n<3):
        return 1
    elif (n < 5):
        return 10
    elif n < 9: 
        return 10000
    else:
        return 1000000

# Kelas untuk menyimpan informasi yang dibutuhkan dalam menyelesaikan permaianan Queens
class QueensSolution:
    
    def __init__(self,grid, updatePapan):
        self.grid   = grid
        self.n      = len(grid)
        self.updatePapan = updatePapan
        self.iterasi = 0
        self.waktuMulai = None
        self.solusi = []
        self.updateInterval = liveUpdate(self.n)
        self.Warna = sorted(set(cell for row in grid for cell in row)) #nyimpen warna unik
    
    def solve(self):
        self.waktuMulai = time.time()
        posisi = [-1] * self.n # -1 kalau blm diisi
        found = self.bruteForce(0,posisi)
        waktuEks = int((time.time() - self.waktuMulai) * 1000)
        return found, self.solusi, self.iterasi, waktuEks
    
    def bruteForce(self, col, posisi):
        if col == self.n:
            self.iterasi += 1

            if self.iterasi % self.updateInterval == 0:
                queens = []
                for c in range(self.n):
                    queens.append((posisi[c],c)) #posisi yang ada queen nya (row,col)
                self.updatePapan(queens, self.iterasi)
            
            if self.isValid(posisi):
                self.solusi = []
                for c in range(self.n):
                    self.solusi.append((posisi[c],c))
                return True
            else:
                return False
            
        for row in range(self.n):
            posisi[col] = row
            self.iterasi += 1

            if self.iterasi % self.updateInterval == 0:
                queens = []
                for c in range(col + 1):
                    queens.append((posisi[c],c))
                self.updatePapan(queens, self.iterasi)

            if self.bruteForce(col+1, posisi):
                return True
        
        posisi[col] = -1
        return False
    
    def isValid(self, posisi):
        n = self.n
        warnaUsed = set()
        for c in range(n):
            r = posisi[c]
            warnaReg = self.grid[r][c]
            if warnaReg in warnaUsed:
                return False
            warnaUsed.add(warnaReg)

        #tiap warna hanya satu queen
        if warnaUsed != set(self.Warna):
            return False
        
        #tiap row hanya satu queen
        if len(set(posisi)) != n:
            return False
        
        #ga bole ada diagonal
        for col1 in range(n):
            for col2 in range (col1 + 1, n):
                if abs(posisi[col1] - posisi[col2]) <= 1 and (col2-col1) == 1:
                    return False
        
        return True






    

    
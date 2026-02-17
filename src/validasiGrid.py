def validasiGrid(grid):
    n = len(grid)

    #ukuran grid harus NxN
    if any(len(row)!=n for row in grid):
        return False, "Input Invalid: grid tidak berukuran NxN"
    
    #jumlah warna harus sama dengan N
    warnaUnik = set(cell for row in grid for cell in row)
    if len(warnaUnik)!= n:
        return False, f"Input Invalid: jumlah warna unik yang diharapkan {n} buah, yang diinput {len(warnaUnik)} buah "
    
    return True, "Valid"
from math import sqrt

def cell_dist(cell1, cell2):
    """Calculate euclidian distance between two cells"""
    x1,y1 = cell1.coordinate
    x2,y2 = cell2.coordinate

    dx = x1-x2
    dy = y1-y2

    return sqrt(dx**2 + dy**2)
from movement.ik_cache import IKCache

from point import Point3D

cache = IKCache('store/ik_cache.json')

cache.cache = {
    str(Point3D(0, 1, 2)): [30, 40, 50],
    str(Point3D(0, 11, 2)): [30, 401, 50],
    str(Point3D(0, 12, 2)): [30, 402, 50]
}

print(cache.export())

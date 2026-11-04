import math
from modele import Vector2D
from wzorce import Polar2DAdapter, Vector3DDecorator, Vector3DInheritance

def main():
    vectors = [
        Vector2D(3, 4),
        Vector2D(-2, 5),
        Vector2D(1, -2)
    ]
    names = ["A", "B", "C"]

    print("\nWspółrzędne wektorów")
    for i, vec in enumerate(vectors):
        cart = vec.get_components()
        polar = Polar2DAdapter(vec)
        
        angle_rad = polar.get_angle()
        angle_deg = angle_rad * 180.0 / math.pi

        print(f"Wektor {names[i]}:")
        print(f"Kartezjańskie: [{cart[0]:.4f}, {cart[1]:.4f}]")
        print(f"Biegunowe: r = {polar.abs():.4f}, kąt = {angle_rad:.4f} rad ({angle_deg:.2f}°)")

    print("\nIloczyn skalarny (wszystkie kombinacje)")
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            dot = vectors[i].c_dot(vectors[j])
            print(f"{names[i]} · {names[j]} = {dot:.4f}")

    print("\nIloczyn wektorowy (wszystkie kombinacje, macierzowo)")
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            #dla wektorów 2D przyjmujemy z = 0. Robione przez Dekorator
            dec = Vector3DDecorator(vectors[i], 0)
            cross_result = dec.cross(vectors[j])
            print(f"{names[i]} × {names[j]} = {cross_result}")

    print("\nTest Vector3DInheritance (pełne 3D)")
    v3d_1 = Vector3DInheritance(1, 2, 3)
    v3d_2 = Vector3DInheritance(-1, 4, 2)
    
    #formatowanie listy do wypisu
    comp1 = ", ".join(f"{x:.4f}" for x in v3d_1.get_components())
    comp2 = ", ".join(f"{x:.4f}" for x in v3d_2.get_components())
    
    print(f"v3d1 = [{comp1}]")
    print(f"v3d2 = [{comp2}]")
    print(f"v3d1 × v3d2 = {v3d_1.cross(v3d_2)}")

if __name__ == "__main__":
    main()
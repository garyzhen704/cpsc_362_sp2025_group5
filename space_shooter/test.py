from object import Object
from vector import Vector

white_box_cases = [
    # (position of obj1,  position of obj2,  whether or not there should be a collision)
    (Vector(0, 0), Vector(10, 0), True),
    (Vector(0, 0), Vector(15, 0), True),
    (Vector(0, 0), Vector(20, 0), True),
    (Vector(0, 0), Vector(25, 0), True),
    (Vector(0, 0), Vector(30, 0), False),
    (Vector(0, 0), Vector(35, 0), False),
    (Vector(0, 0), Vector(40, 0), False),
]

def white_box_test():    
    obj1 = Object(10, Vector(0, 0), Vector(0, 0), (0, 0, 0))
    obj2 = Object(20, Vector(0, 0), Vector(0, 0), (0, 0, 0))

    print(f"Object 1: radius = {obj1.hitbox.radius}")
    print(f"Object 2: radius = {obj2.hitbox.radius}")

    i = 1
    for case in white_box_cases:
        print(f"Test case {i}:")
        obj1.position = case[0]
        obj2.position = case[1]

        print(f"    Object 1 position: {obj1.position}")
        print(f"    Object 2 position: {obj2.position}")

        if case[2]:
            print("    Expecting a collision")
        else:
            print("    Expecting no collision")

        collision = obj1.hitbox.is_colliding(obj2)
        if collision:
            print("    Collision detected")
        else:
            print("    Collision not detected")
        
        if collision == case[2]:
            print("    Test passed")
        else:
            print("    Test failed")

        print("")
        i += 1


test_fps = 60
black_box_cases = [60, 30, 20, 10, 500]  # velocities to test

def black_box_test():
    i = 1
    for speed in black_box_cases:
        print(f"Test case {i}, speed = {speed}")

        obj = Object(10, Vector(0, 0), Vector(speed, 0), (0, 0, 0))
        expected_pos = Vector(speed / test_fps, 0)

        print(f"    Object initial position: {obj.position}")
        print(f"    Object initialized with velocity {obj.velocity}, next position should be {expected_pos}")

        obj.update(test_fps)

        print(f"    Object final position: {obj.position}")

        if obj.position.x == expected_pos.x \
        and obj.position.y == expected_pos.y:
            print("    Test passed")
        else:
            print("    Test failed")
    
        print("")
        i += 1


white_box_test()
black_box_test()

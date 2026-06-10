import gc
import sys
import weakref

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None        

    def __repr__(self):
        return f"Node({self.name!r})"

    def __del__(self):
        print(f"  [__del__]  {self.name} is being destroyed")


def banner(text):
    print(f"\n--- {text} ---")


def main():
    gc.disable()
    gc.collect()

    banner("Step 1 — create the cycle  A <-> B")
    A = Node("A")
    B = Node("B")
    A.link = B
    B.link = A
    print(f"  A = {A},  A.link = {A.link}")
    print(f"  B = {B},  B.link = {B.link}")

    a_weak = weakref.ref(A)
    b_weak = weakref.ref(B)

    banner("Step 2 — refcounts before del")
    print(f"  sys.getrefcount(A) = {sys.getrefcount(A)}  "
          f"(local 'A' + B.link + argument to getrefcount)")
    print(f"  sys.getrefcount(B) = {sys.getrefcount(B)}  "
          f"(local 'B' + A.link + argument to getrefcount)")

    banner("Step 3 — del A; del B")
    del A
    del B
    print("  del statements ran, but no __del__ message yet.")

    banner("Step 4 — are they really still in memory?")
    still_a = a_weak()      
    still_b = b_weak()
    print(f"  weakref to A resolves to: {still_a!r}")
    print(f"  weakref to B resolves to: {still_b!r}")
  
    del still_a, still_b

    
    leaked = [o for o in gc.get_objects() if isinstance(o, Node)]
    print(f"  gc.get_objects() reports {len(leaked)} live Node(s): {leaked}")
    del leaked   

    banner("Step 5 — gc.collect()")
    unreachable = gc.collect()
   
    print(f"  gc.collect() reclaimed {unreachable} unreachable object(s).")

  
    banner("Step 6 — after collection")
    print(f"  a_weak() -> {a_weak()}    (None means object is gone)")
    print(f"  b_weak() -> {b_weak()}    (None means object is gone)")

    gc.enable()


if __name__ == "__main__":
    main()
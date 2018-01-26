import time
import types

class Ant:
    def __init__(self, role):
        self.role_funcs = [self.step_A, self.step_B]

        self.counter = 0

        self._role = None
        self.role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        self._role = new_role
        self.step = self.role_funcs[new_role]

    def step_A(self):
        self.counter += 1

    def step_B(self):
        self.counter += 1




# class Ant:
#     def __init__(self, role):
#         self.role = role
#         self.counter = 0
#
#     @property
#     def role(self):
#         return self.role
#
#     @role.setter
#     def role(self, new_role):
#         self.step = types.MethodType(new_role, self)
#
# def Active(self):
#     self.counter += 1
#
# def Inactive(self):
#     self.counter += 1

class Ant:
    def __init__(self, role):
        self._role = None
        self.role = role
        self.counter = 0

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        self._role = new_role

    def step(self):
        self.role.step(self)

class Inactive:
    def step(self):
        self.counter += 0

class Active:
    def step(self):
        self.counter += 1

class User:
    def get_password():
        pass

    def get_name():
        pass


User.get_password()


ant = Ant(0)
start = time.clock()
for _ in range(1000000):
    ant.role = 0
    ant.step()
    ant.role = 1
    ant.step()
end = time.clock()

print("Took: ", end - start)
print(ant.counter)


    #
    # def get_neighbors(self):
    #     x, y = self.pos
    #
    #     neighbors = self.model.grid.grid[x][y]
    #
    #     if neighbors:
    #         self.role = random.choice(list(neighbors)).role
    #
    #     # for neigh in neighbors:
    #     #     self.role = neigh.role
    #     #     break

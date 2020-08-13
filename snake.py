import tkinter as tk
from PIL import ImageTk,Image
from random import randint



MOVE=20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.snake_positions=[(100,100),(80,100),(60,100)]
        self.food_position=self.new_food_position()
        self.score=0
        self.direction="Right"
        self.bind_all("<Key>",self.on_key_press)

        self.load_asset()
        self.create_objects()
        


        self.after(75,self.perform_actions)

    def load_asset(self):
          try:
              self.snake_body_image = Image.open("snake.png")
              self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

              self.food_image = Image.open("food.png")
              self.food = ImageTk.PhotoImage(self.food_image)
          except IOError as error:
              root.destroy()
              raise

    
    def create_objects(self):
        self.create_text(35, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10)

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69") 


    def move_snake(self):
        head_position_x,head_position_y=self.snake_positions[0]
        new_head_position=(head_position_x+MOVE,head_position_y)

        if self.direction == "Left":
            new_head_position = (head_position_x - MOVE, head_position_y)
        elif self.direction == "Right":
            new_head_position = (head_position_x + MOVE, head_position_y)
        elif self.direction == "Down":
            new_head_position = (head_position_x, head_position_y + MOVE)
        elif self.direction == "Up":
            new_head_position = (head_position_x, head_position_y - MOVE)


        self.snake_positions=[new_head_position]+self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)
    
    def perform_actions(self):
        if self.check_collision():
            self.end_game()
            return

        self.move_snake()
        self.food_collision()
        self.after(GAME_SPEED,self.perform_actions)

    def check_collision(self):
        head_position_x,head_position_y=self.snake_positions[0]

        return (head_position_x in (0,600) or head_position_y in (20,620) or (head_position_x,head_position_y) in self.snake_positions[1:])


    def on_key_press(self,e):
        new_direction=e.keysym
        all_directions=("Left","Right","Up","Down")
        opposites=({"Up","Down"},{"Left","Right"})

        if (new_direction in all_directions and {new_direction,self.direction} not in opposites):
            self.direction=new_direction
    
    def food_collision(self):
        if self.snake_positions[0]==self.food_position:
            self.score +=1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")

            
            self.food_position = self.new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score=self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE
            y_position = randint(3, 30) * MOVE
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position
    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14
        )
        


root=tk.Tk()
root.title("SNAKE CLASSIC")
root.resizable(False,False)
root.tk.call("tk", "scaling", 4.0)

img=tk.PhotoImage(file="icon.png")
root.tk.call("wm","iconphoto",root._w,img)

board=Snake()
board.pack()
root.mainloop()
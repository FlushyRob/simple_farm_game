import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


# Implement your classes here


def play_game(root: tk.Tk, map_file: str) -> None:
    """
    • Constructs controller instance using given map file and root tk.Tk
      parameter.
    • Ensure root window stays opening listening for events (using mainloop).

    Parameters:
        root : tkinter.Tk
            Main window game is displayed.
        map_file : str
            File path to game map file containing rectangular grid of characters
            representing layout of game world.
    """
    FarmGame(root, map_file)
    root.mainloop()


# Views
class FarmView(AbstractGrid):
    """
    Inherits from AbstractGrid. Grid displaying farm map, player, and plants.
    """
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int],
                 size: tuple[int, int], **kwargs) -> None:
        """
        Sets up FarmView as AbstractGrid with appropriate dimensions and
        size. Creates instance attribute of empty dictionary to be used as image
        cache.

        Parameters:
            master (tk.Tk | tk.Frame):
                Parent widget to place this frame in. Can be Tk root window or
                tk.Frame instance.
            dimensions (tuple[int, int]):
                Number of rows and columns in grid.
            size (tuple[int, int]):
                Width and height of each cell in grid.
        """
        super().__init__(master, dimensions, size, **kwargs)
        self._farm_view_cache = {}
        self.CELL_WIDTH, self.CELL_HEIGHT = self.get_cell_size()

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], "Plant"],
               player_position: tuple[int, int], player_direction: str) -> None:
        """
        Clears farm view, then creates (on FarmView instance) images for ground,
        then plants, then player. Player and plants should render in front of
        ground, and player should render in front of plants.

        Parameters:
            ground (list[str]):
                List of strings representing ground tiles in farm.
            plants (dict[tuple[int, int], Plant]):
                Dictionary mapping coordinates of plants to plant objects.
            player_position (tuple[int, int]):
                Coordinates of player in farm.
            player_direction (str):
                Direction player is facing.
        """
        # clear farm view
        self.clear()

        # create images for ground and plants and player
        self.draw_map(ground)
        self.draw_plants(plants)
        self.draw_player(player_position, player_direction)

    def draw_image_at_tile(self, image: tk.PhotoImage, row: int, 
                           column: int) -> None:
        """
        Draws given image at given row and column in abstract grid.

        Parameters:
            image (tk.PhotoImage):
                Image to be drawn.
            row (int):  
                Row number of cell to draw image in.
            column (int):
                Column number of cell to draw image in.
        """
        # translate row to pixel location
        x_position, y_position = self.get_midpoint((row, column))

        # draw image at pixel location
        self.create_image(x_position, y_position, image=image)

    def draw_map(self, ground: list[str]) -> None:
        """
        Creates (on FarmView instance) images for ground.

        Parameters:
            ground (list[str]):
                List of strings representing ground tiles in farm.
        """
        width = self.CELL_WIDTH
        height = self.CELL_HEIGHT
        # Get images of ground
        grass_image = get_image("images/grass.png", (width, height), 
                                self._farm_view_cache)
        soil_image = get_image("images/soil.png", (width, height),
                               self._farm_view_cache)
        untilled_soil_image = get_image("images/untilled_soil.png", 
                                        (width, height), self._farm_view_cache)

        # Draw an image at each tile of corresponding ground type
        row_number = -1
        column_number = -1

        # draw picture for each tile
        for row in ground:
            row_number += 1
            column_number = -1

            for column in row:
                column_number += 1

                if column == GRASS:
                    self.draw_image_at_tile(
                        grass_image, row_number, column_number)
                elif column == SOIL:
                    self.draw_image_at_tile(
                        soil_image, row_number, column_number)
                elif column == UNTILLED:
                    self.draw_image_at_tile(
                        untilled_soil_image, row_number, column_number)

    def draw_plants(self, plants: dict[tuple[int, int], Plant]) -> None:
        """
        Draws plants on farm view.

        Parameters:
            plants (dict[tuple[int, int], Plant]):
                Dictionary mapping coordinates of plants to plant objects.
        """
        for (row, column), plant_class in plants.items():
            
            # find plant image
            plant_stage = plant_class.get_stage()
            plant_name = plant_class.get_name()
            plant_image = get_image(
                f"images/plants/{plant_name}/stage_{plant_stage}.png", 
                (self.CELL_WIDTH, self.CELL_HEIGHT), self._farm_view_cache)
            
            self.draw_image_at_tile(plant_image, row, column)

    def draw_player(self, player_position: tuple[int, int], 
                    player_direction: str) -> None:
        """
        Creates (on FarmView instance) image for player. Uses get_image function
        (a3_support.py) to create image.

        Parameters:
            player_position (tuple[int, int]):
                Coordinates of player in farm.
            player_direction (str):
                Direction player is facing.
        """
        # Get image of player
        player_image = get_image(f"images/{IMAGES[player_direction]}",
                                 (self.CELL_WIDTH, self.CELL_HEIGHT), 
                                 self._farm_view_cache)

        # Draw image of player
        self.draw_image_at_tile(
            player_image, player_position[0], player_position[1])


class InfoBar(AbstractGrid):
    """
    Inherits from AbstractGrid. Grid with 2 rows and 3 columns displaying info
    to user about number of days elapsed in game, player's energy, and money.
    Spans width of farm and inventory combined.
    """
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """
        Sets up InfoBar as AbstractGrid with appropriate number of rows and
        columns, and appropriate width and height from constants.py.

        Parameters:
            master (tk.Tk | tk.Frame):
                Parent widget to place this frame in. Can be Tk root window or
                tk.Frame instance.
        """
        super().__init__(master, (2, 3), 
                         (FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT))
        self.draw_infobar_headings()

    def redraw(self, day: int, money: int, energy: int) -> None:
        """
        Clears InfoBar and redraws it to display provided day, money, and
        energy.

        Parameters:
            day (int):
                Number of days elapsed in game.
            money (int):
                Amount of money player has.
            energy (int):
                Amount of energy player has.
        """
        self.clear()
        self.draw_infobar_headings()

        # Write data for each column
        font = ("Helvetica", 15)
        annotations = [(0, day), (1, f"${money}"), (2, energy)]
        for annotation in annotations:
            self.annotate_position((1, annotation[0]), annotation[1], font)

    def draw_infobar_headings(self) -> None:
        """
        Draws headings for each column in InfoBar. Called on initialisation and
        after each clear() method.
        """
        headings = ["Day:", "Money:", "Energy:"]
        for index, heading in enumerate(headings):
            self.annotate_position((0, index), heading, HEADING_FONT)


class ItemView(tk.Frame):
    """
    Inherits from tk.Frame. Frame displaying information and buttons for
    single item. There are 6 items in game (see ITEMS in constants.py).
    ItemView for item should contain following widgets, packed left to
    right:
        • Label containing item's name, amount in player's inventory, selling
            price, and buying price of item (if item is buyable; see BUY PRICES in constants.py).
        • If item is buyable, frame should contain button for buying item at
          buy price.
        • button for selling item at sell price (all items are sellable).
    There are three of events that can occur on ItemView:
        • Left click on item's frame or label (indicating user's wish to
          select item).
        • Button press on buy button (indicating user's wish to buy one of
          those items).
        • Button press on sell button (indicating user's wish to sell one of
          those items).
    Callbacks for these buttons is created in controller (see FarmGame) and
    passed to each ItemView via constructor.
    """

    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """
        Sets up ItemView to operate as tk.Frame. Creates all internal widgets.
        Sets commands for buy and sell buttons to buy command and sell command
        each called with appropriate item name respectively. Binds select
        command to be called with appropriate item name when ItemView frame or
        label is left clicked.

        Parameters:
            master (tk.Frame):
                Parent widget to place this frame in. Can be tk.Frame instance.

            item_name (str):
                Name of item to display.

            amount (int):
                Amount of item player has.

            select_command (Optional[Callable[[str], None]]):
                Callback to be called when item is selected.

            sell_command (Optional[Callable[[str], None]]):
                Callback to be called when item is sold.

            buy_command (Optional[Callable[[str], None]]):
                Callback to be called when item is bought.
        """
        # creates a frame for the item view
        super().__init__(master, width=INVENTORY_WIDTH, height=FARM_WIDTH // 6,
                         highlightbackground="#d68f54", highlightthickness=1,
                         background="#fdc074")
        
        # set frame's pack propagate to false
        self.pack_propagate(False)

        # get amount, selling price, and buying price. 
        try:
            self._buy_price = f"${BUY_PRICES[item_name]}"
        except KeyError:
            self._buy_price = "$N/A"
        self._item_name = item_name
        self._sell_price = f"${SELL_PRICES[item_name]}"

        # create info label
        self._item_info_label = tk.Label(self, bg="#fdc074", 
            text=f"{self._item_name}: {amount}\nSell price: \
            {self._sell_price}\nBuy price: {self._buy_price}")
        
        # bind click event to pass item name to select command
        self._item_info_label.bind("<Button-1>", 
                                  lambda event: select_command(self._item_name))

        # pack info label into large info frame
        self._item_info_label.pack(side=tk.LEFT, expand=True)

        # create and pack buy button for seeds
        if self._buy_price != "$N/A":
            self._buy_button = tk.Button(self, text="Buy",
                                         command=lambda item=self._item_name: buy_command(item))
            self._buy_button.pack(side=tk.LEFT, expand=True)

        # create and pack sell button
        self._sell_button = tk.Button(self, text="Sell",
                        command=lambda item=self._item_name: sell_command(item))
        self._sell_button.pack(side=tk.LEFT, expand=True)

        # Bind a left click on frame to pass in item name into select command
        self.bind("<Button-1>", lambda event: select_command(self._item_name))

    def update(self, amount: int, selected: bool = False) -> None:
        """
        Updates text on label, and colour of this ItemView. Called by controller
        when model changes.
        """
        # update label text
        self._item_info_label.config(
            text=
            f"{self._item_name}: {amount}\nSell price: \
{self._sell_price}\nBuy price: {self._buy_price}")
        
        # update colour of item view
        self._item_info_label.config(bg="#fdc074")
        self.config(background="#fdc074")

        if selected == True and self._item_name in ["Potato Seed", "Kale Seed",
                                                    "Berry Seed"]:
            self._item_info_label.config(bg="#d68f54")
            self.config(background="#d68f54")

        if amount == 0:
            self._item_info_label.config(bg="grey")
            self.config(background="grey")

# Controller Class
class FarmGame:
    """
    Controller class for game. Responsible for creating and maintaining
    instances of model and view classes, event handling, and facilitating
    communication between model and view classes.
    """

    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        Sets up FarmGame. Does the following:
            • Set title of window.
            • Create title banner.
            • Create FarmModel instance.
            • Create instances of your view classes, and display them.
            • Create button to enable users to increment day. Has text
              "Next day" displayed below other view classes. When this button is
              pressed, model advances to next day, then view classes are redrawn
              to reflect changes in model.
            • Bind handle keypress method to "<KeyPress>" event.
            • Call redraw method to ensure view draws according to current model
              state.

        Parameters:
            master (tk.Tk):
                Tk root window.
            map_file (str):
                Name of file containing map data.
        """
        # Create main window
        self._master = master
        master.title("Farm Game")

        # Initialize cache and display title header
        self._cache = {}
        header_file = get_image("images/header.png",
                                (FARM_WIDTH + INVENTORY_WIDTH, BANNER_HEIGHT), 
                                self._cache)
        _header_image = tk.Label(master, image=header_file)
        _header_image.pack()

        # Create and pack middle frame for FarmView and ItemView
        # Create and pack bottom frame for InfoBar.
        self._middle_frame = tk.Frame(master)
        self._middle_frame.pack(side=tk.TOP, fill=tk.X)
        self._bottom_frame = tk.Frame(master)
        self._bottom_frame.pack(side=tk.TOP, fill=tk.X)

        # Initiate FarmModel and establish some variables
        self.FarmModel = FarmModel(map_file)
        self._player = self.FarmModel.get_player()

        

        # Initiate FarmView
        self.list_map = read_map(map_file)
        map_rows = len(self.list_map)
        map_columns = len(self.list_map[0])
        self.FarmView = FarmView(self._middle_frame,
                                        (map_rows, map_columns), 
                                        (FARM_WIDTH, FARM_WIDTH))

        # Initiate six ItemViews - one per item type and pack into item view frame
        self.ItemsView = tk.Frame(
            self._middle_frame, bg="#fdc074", highlightbackground="#d68f54", highlightthickness=2)

        self._player_inventory = ((self.FarmModel).get_player()).get_inventory()
        
        self._selected_seed = None
        self.panels = []

        for item in ITEMS:
            try:
                item_count_in_inventory = self._player_inventory[item]
            except KeyError:
                item_count_in_inventory = 0

            self._small_item_view = ItemView(self.ItemsView, item, item_count_in_inventory, self.select_item, self.sell_item, 
                                                 self.buy_item)

            self.panels += [self._small_item_view]

        for panel in self.panels:
            panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initiate info bar
        self.InfoView = InfoBar(self._bottom_frame)

        # pack all three views
        self.FarmView.pack(side=tk.LEFT)
        self.InfoView.pack(side=tk.TOP)
        self.ItemsView.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # create and pack next day button into frame
        self._next_day_button = tk.Button(self._bottom_frame, text="Next day",command=self.next_day)
        self._next_day_button.pack(side=tk.TOP)

        # Redraw everything
        self.redraw()

        # bind keypress to event handler
        self._master.bind("<KeyPress>", self.handle_keypress)

    def next_day(self) -> None:
        """
        Advances game to next day, updating model and view as necessary.
        """
        (self.FarmModel).new_day()
        self.redraw()

    def redraw(self) -> None:
        """
        Redraws entire game based on current model state.
        """
        # Retrieve some information from model
        farm_model = self.FarmModel
        player = farm_model.get_player()
        
        day_count = (farm_model).get_days_elapsed()
        FarmModel_plants = farm_model.get_plants()
        map = farm_model.get_map()

        player_money = (player).get_money()
        player_energy = (player).get_energy()
        player_position = (player).get_position()
        player_direction = (player).get_direction()
        player_inventory = (player).get_inventory()

        # clear farm view and redraw
        (self.FarmView).clear()
        (self.FarmView).redraw(map, FarmModel_plants, player_position, 
                               player_direction)

        (self.InfoView).redraw(day_count, player_money, player_energy)


        # get a list of how many items there are
        item_count_list = []
        for item in ITEMS:
            try:
                item_count_in_inventory = player_inventory[item]
            except KeyError:
                item_count_in_inventory = 0
            item_count_list.append(item_count_in_inventory)
        
        # get index of selected item
        selected_index = None
        index = -1
        for panel in self.panels:
            index += 1
            if self._selected_seed == panel._item_name:
                selected_index = index
                break

        # update all item views and reset all selected item view's colours
        for index in range(0, 6):
            self.panels[index].update(item_count_list[index])
        
        # update selected item view and colour selected panel
        try:
            self.panels[selected_index].update(item_count_list[selected_index], 
                                               True)
        except TypeError:
            pass
        

    def handle_keypress(self, event: tk.Event) -> None:
        """
        Event handler. Called when keypress event occurs. Triggers relevant
        behaviour and updates views to reflect changes:
        • "w", "a", "s", "d" move player up, left, down, right respectively.
        • "p" attempts to plant selected seed at player's current position if
            position contains soil and no plant exists.
        • "h" attempts to harvest plant at player's current position if it is
            ready for harvest, adding harvested items to player's inventory and
            removing plant if necessary.
        • 'r' attempts to remove plant at player's current position, regardless
           of its maturity.
        • 't' attempts to till soil at player's current position if it is
           untilled.
        • 'u' attempts to untill soil at player's current position if it is
           tilled and does not contain plant.
        • Left-clicking on item in inventory selects it as active item.
        • Buy button attempts to buy selected item.
        • Sell button attempts to sell one of selected item from player's
          inventory.
        If key not corresponding to event is pressed, it is ignored.

        Parameters:
            event (tk.Event):
                Event object containing information about event that triggered
                this callback.
        """
        # define reoccuring variables
        farm_model = self.FarmModel
        player = farm_model.get_player()
        player_position = (player).get_position()
        plants_info = farm_model.get_plants()
        row, column = player_position
        map = farm_model.get_map()
        map_tile = map[row][column]
        movement_keys = {"w": UP,
                         "a": LEFT,
                         "s": DOWN,
                         "d": RIGHT}

        if event.char in movement_keys:
            # move player
            farm_model.move_player(movement_keys[event.char])

        elif event.char == "p":
            # make sure player's position is soil
            if map_tile != SOIL:
                return
            
            # make sure player's location doesn't have existing plant
            if player_position in plants_info:
                return

            # make sure selected item is a seed
            if self._selected_seed == None:
                return
            
            # make sure the player has at least 1 item
            try:
                if (player).get_inventory()[self._selected_seed] <= 0:
                    return
            except KeyError:
                return
            
            selected_items_words = self._selected_seed.split()
            if selected_items_words[1] != "Seed":
                return
            
            plant_name = selected_items_words[0].lower()

            # find relevent plant class
            for plant_class in [PotatoPlant(), KalePlant(), BerryPlant()]:
                if plant_class.get_name() == plant_name:
                    unique_plant = plant_class
            
            # add plant to farm model. If successful, remove seed from player
            if farm_model.add_plant(player_position, unique_plant) == True:
                player.remove_item((self._selected_seed, 1))

        elif event.char == "h":
            # make sure this location has a plant
            if player_position not in plants_info:
                return
            
            # make sure plant is at stage 5
            if (plants_info[player_position]).can_harvest() == False:
                return

            # harvest plant
            harvested_item, amount = farm_model.harvest_plant(player_position)
            (player).add_item((harvested_item, amount))
        
        elif event.char == "r":
            # make sure player is standing at a plant
            if player_position not in plants_info:
                return
            
            # remove plant
            farm_model.remove_plant(player_position)

        elif event.char == "t":
            # till soil
            farm_model.till_soil(player_position)

        elif event.char == "u":
            # untill soil
            farm_model.untill_soil(player_position)

        self.redraw()

    def select_item(self, item_name: str) -> None:
        """
        Sets selected item to be item name then redraws view.

        Parameters:
            item_name (str):
                Name of item to be selected.
        """
        self._selected_seed = item_name
        self.redraw()

    def buy_item(self, item_name: str) -> None:
        """
        Causes player to attempt to buy item with given item name at price
        specified in BUY_PRICES, then redraw view.

        Parameters:
            item_name (str):
                Name of item to be bought.
        """
        player = self.FarmModel.get_player()
        player.buy(item_name, BUY_PRICES[item_name])

        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """
        Causes player to attempt to sell item with given item name at price
        specified in SELL_PRICES, then redraw view.

        Parameters:
            item_name (str):
                Name of item to be sold.
        """
        player = self.FarmModel.get_player()
        player.sell(item_name, SELL_PRICES[item_name])
        
        self.redraw()


def main():
    """
    Constructs controller instance and begins event loop.
    """
    root = tk.Tk()
    MAP_PATH = "maps\map1.txt"
    play_game(root, MAP_PATH)


if __name__ == "__main__":
    main()

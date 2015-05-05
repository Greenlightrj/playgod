Read me for PlayGod
created by Rebecca Jordan, Caz Nichols, and Marie-Caroline Finke for Spring 2015 SoftDes at Olin COllege of Engineering

Instructions:
The goal of the game is to reach a set environment and have at least 10 bugs survive in the goal environment for a longer period of time.
To start run main.py in your terminal, this will open a new window. Click anywhere in the new window to start. This will navigate you onto a light green window containing the following:
- Bugs: Multicolored square sprites with four legs. Each bug has a genome consisting of the following:
	- camoflouge (how well the bugs blend in with the environment, represented by color)
	- speed (how fast the bugs are, represented by leg-length)
	- hunting (how well they can hunt Noms, represented by fang length)
	- cold resistance (how well the Bugs survive in cold weather, represented by fur length)
	- drought resistance (how much water the bugs need to survive, represented by having a larger belly)
- Noms: small black flies floating around the screen. These are the food source of the Bugs. If a Bug doesn't eat enough Noms it will starve. Noms can also kill a Bug if the Bugs hunting stat isn't high enough
- Rawrs: green, plant-like monsters chasing the Bugs. These are the predator of the Bugs. If a Rawr catches a Bug the Bug will die. 
- Blue puddles: these are the water sources for the Bugs. Bugs will die of thirst if they don't drink enough water but they can also die if they are too drought resistant and collide with water. Puddles will spawn naturally and the amount will depend on the moisture of the environment.
- A row of buttons in the top-left: clicking each of these buttons will spawn the element shown on the button. Spawning a new element costs money. The environmental elements each effect the environment according to their type. The types are desert, rainforest, and arctic. A desert element will lower the moisture and raise the heat, a jungle element will raise the moisture and raise the heat, an arctic element will lower the moisture and lower the heat. The waterdroplet willll spawn more puddles.
- The information panel on the right: this panel gives you information about the state of the game. From top to bottow it lists the amount of Money you currently posses, the heat and the moisture, the number of living bugs, graphs showing how each attribute of the genome is changing over time, and the cuase of death seperated into categories.

Any other questions? Find a glitch? Contact us on sites.google.com/site/playgodproject/home



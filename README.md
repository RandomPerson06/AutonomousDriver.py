# Autonomous Driving using NeuroEvolution of Augmenting Topologies
## Overview
AutonomousDriver is a project that uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve neural networks for autonomous driving. The project allows users to train and test neural networks on custom maps.

## Installation
Clone the repository:
```
git clone https://github.com/buzzpranav/AutonomousDriver.py
cd AutonomousDriver.py
```
Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage
```
python SelfDrive.py
```
## Code Overview
### Car Class
- Initialization: Sets up the car's properties, including its position, speed, radar sensors, and visual representation.
- Drawing: Methods to draw the car and its radar on the screen, providing a visual indicator of what the car "sees."
- Collision Detection: Checks for collisions with the map borders, determining if the car is still "alive."
- Radar: Simulates radar sensors to detect distances to obstacles, feeding this information to the neural network.
- Update: Updates the car's position, rotation, and checks for collisions, driving the simulation forward.
- Data and Reward: Methods to retrieve radar data for the neural network and calculate the reward based on the distance traveled.
### run_simulation Function
- Initialization: Sets up the NEAT neural networks and car instances for the current generation.
- Simulation Loop: Runs the main simulation loop, updating car positions, handling neural network outputs, and checking for collisions.
- Fitness Calculation: Adjusts the fitness scores based on the car's performance and renders the simulation on the screen.
### plot_fitness Function
- Real-time Plotting: Uses Matplotlib to plot the average fitness scores over generations, providing a visual tool to monitor the progress of the AI.
### Main Function
- Initialization: Sets up Pygame and NEAT configurations, including the game display and NEAT parameters.
- Threading: Runs the simulation and fitness plotting in separate threads, ensuring the simulation remains responsive while updating the fitness plot.

## Custom Maps
You can use your own maps for training and testing. Simply create a map using a simple drawing tool like MS Paint and save it as an image file. Upload the image to the maps folder in the project directory.

### Steps to Create a Custom Map
1. Open MS Paint or any other simple drawing tool.
2. Draw your map. Ensure that the roads and paths are clearly defined.
3. Save the image as a .png or .jpg file.
4. Upload the image to the maps folder in the project directory with the name map\[number].
5. Update variable racemap in SelfDrive.py to your new map number

## Configuration
The project uses a configuration file (config.txt) to set various parameters for the NEAT algorithm. It is optimized and should not be changed unless you know what you are doing:

### NEAT
- fitness_criterion: Determines how fitness is evaluated. Options are max, min, or mean.
- fitness_threshold: The fitness level required to consider the problem solved.
- pop_size: The population size for each generation.
- reset_on_extinction: If True, the population is reset if all species go extinct.

### DefaultGenome
- Node Activation Options
- activation_default: Default activation function for nodes (e.g., tanh).
- activation_mutate_rate: Probability of mutating the activation function.
- activation_options: List of possible activation functions.

### Node Aggregation Options
- aggregation_default: Default aggregation function for nodes (e.g., sum).
- aggregation_mutate_rate: Probability of mutating the aggregation function.
- aggregation_options: List of possible aggregation functions.

### Node Bias Options
- bias_init_mean: Mean of the initial bias values.
- bias_init_stdev: Standard deviation of the initial bias values.
- bias_max_value: Maximum bias value.
- bias_min_value: Minimum bias value.
- bias_mutate_power: Standard deviation of the bias mutation.
- bias_mutate_rate: Probability of mutating the bias.
- bias_replace_rate: Probability of replacing the bias.

### Genome Compatibility Options
- compatibility_disjoint_coefficient: Coefficient for disjoint genes in compatibility calculation.
- compatibility_weight_coefficient: Coefficient for weight differences in compatibility calculation.

### Connection Add/Remove Rates
- conn_add_prob: Probability of adding a new connection.
- conn_delete_prob: Probability of deleting an existing connection.

### Connection Enable Options
- enabled_default: Default state of new connections (enabled or disabled).
- enabled_mutate_rate: Probability of mutating the enabled state of a connection.

### Network Parameters
- feed_forward: If True, the network is feed-forward only.
- initial_connection: Initial connection pattern (e.g., full).
- num_hidden: Number of hidden nodes.
- num_inputs: Number of input nodes.
- num_outputs: Number of output nodes.

### Node Response Options
- response_init_mean: Mean of the initial response values.
- response_init_stdev: Standard deviation of the initial response values.
- response_max_value: Maximum response value.
- response_min_value: Minimum response value.
- response_mutate_power: Standard deviation of the response mutation.
- response_mutate_rate: Probability of mutating the response.
- response_replace_rate: Probability of replacing the response.

### Connection Weight Options
- weight_init_mean: Mean of the initial weight values.
- weight_init_stdev: Standard deviation of the initial weight values.
- weight_max_value: Maximum weight value.
- weight_min_value: Minimum weight value.
- weight_mutate_power: Standard deviation of the weight mutation.
- weight_mutate_rate: Probability of mutating the weight.
- weight_replace_rate: Probability of replacing the weight.

### DefaultSpeciesSet
- compatibility_threshold: Threshold for compatibility between genomes.

### DefaultStagnation
- species_fitness_func: Function to evaluate species fitness (e.g., max).
- max_stagnation: Maximum number of generations a species can stagnate before being removed.
- species_elitism: Number of top species to protect from stagnation.

### DefaultReproduction
- elitism: Number of top genomes to protect from being replaced.
- survival_threshold: Proportion of the population that survives to the next generation.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

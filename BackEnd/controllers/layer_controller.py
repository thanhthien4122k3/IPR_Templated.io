# controllers/layer_controller.py
import copy

from BackEnd.models.layer_model import LayerModel

class LayerController:
    def __init__(self, layerList_model):
        """Initialize the layer controller with a layer list model."""
        self.layerList_model = layerList_model  # LayerList to store layers
        self.layers = layerList_model.layers if hasattr(layerList_model, 'layers') else []  # List of LayerModel instances
        self.selected_layer = None  # Currently selected layer

    def add_layer(self, obj, name=None):
        """Add a new layer with the given object."""
        layer = LayerModel(obj, name)
        layer.order = len(self.layers)  # Set order to the topmost
        self.layers.append(layer)
        return layer

    def delete_layer(self, layer):
        """Remove a layer from the list."""
        if layer in self.layers:
            self.layers.remove(layer)
            if self.selected_layer == layer:
                self.selected_layer = None
            # Update orders of remaining layers
            for i, l in enumerate(self.layers):
                l.order = i

    def duplicate_layer(self, layer):
        """Create a duplicate of the given layer."""
        if layer in self.layers:
            new_obj = copy.deepcopy(layer.object)
            new_layer = LayerModel(new_obj, f"{layer.name} (Copy)")
            new_layer.x = layer.x + 20  # Offset position
            new_layer.y = layer.y + 20
            new_layer.width = layer.width
            new_layer.height = layer.height
            new_layer.rotation = layer.rotation
            new_layer.order = len(self.layers)  # Add to top
            self.layers.append(new_layer)
            return new_layer
        return None

    def move_layer_up(self, layer):
        """Move the layer up one position in the order."""
        if layer in self.layers:
            idx = self.layers.index(layer)
            if idx < len(self.layers) - 1:
                self.layers[idx], self.layers[idx + 1] = self.layers[idx + 1], self.layers[idx]
                self.layers[idx].order = idx
                self.layers[idx + 1].order = idx + 1

    def move_layer_down(self, layer):
        """Move the layer down one position in the order."""
        if layer in self.layers:
            idx = self.layers.index(layer)
            if idx > 0:
                self.layers[idx], self.layers[idx - 1] = self.layers[idx - 1], self.layers[idx]
                self.layers[idx].order = idx
                self.layers[idx - 1].order = idx - 1

    def move_layer_to_top(self, layer):
        """Move the layer to the top of the order."""
        if layer in self.layers:
            self.layers.remove(layer)
            self.layers.append(layer)
            for i, l in enumerate(self.layers):
                l.order = i

    def move_layer_to_bottom(self, layer):
        """Move the layer to the bottom of the order."""
        if layer in self.layers:
            self.layers.remove(layer)
            self.layers.insert(0, layer)
            for i, l in enumerate(self.layers):
                l.order = i

    def select_layer(self, layer):
        """Select a specific layer."""
        if layer in self.layers:
            if self.selected_layer:
                self.selected_layer.selected = False
            self.selected_layer = layer
            layer.selected = True

    def select_layer_at_point(self, mouse_x, mouse_y):
        """Select a layer at the given mouse coordinates."""
        for layer in reversed(self.layers):  # Check from topmost layer
            if layer.visible and not layer.locked and layer.is_point_inside(mouse_x, mouse_y):
                self.select_layer(layer)
                return layer
        # Deselect if no layer is found
        if self.selected_layer:
            self.selected_layer.selected = False
            self.selected_layer = None
        return None

    def toggle_layer_visibility(self, layer):
        """Toggle the visibility of a layer."""
        if layer in self.layers:
            layer.visible = not layer.visible

    def toggle_layer_lock(self, layer):
        """Toggle the lock state of a layer."""
        if layer in self.layers:
            layer.locked = not layer.locked

    def update_layer_name(self, layer, new_name):
        """Update the name of a layer."""
        if layer in self.layers:
            layer.name = new_name

    def move_layer(self, layer, dx, dy):
        """Move the layer by a specified offset."""
        if layer in self.layers and not layer.locked:
            layer.move(dx, dy)

    def rotate_layer(self, layer, angle):
        """Rotate the layer by a specified angle."""
        if layer in self.layers and not layer.locked:
            layer.rotate(angle)

    def resize_layer(self, layer, width, height, x=None, y=None):
        """Resize the layer to new dimensions, optionally updating position."""
        if layer in self.layers and not layer.locked:
            layer.resize(width, height, x, y)

    def get_layers(self):
        """Return the list of all layers, sorted by order."""
        return sorted(self.layers, key=lambda l: l.order)

    def get_visible_layers(self):
        """Return the list of visible layers, sorted by order."""
        return [layer for layer in self.get_layers() if layer.visible]
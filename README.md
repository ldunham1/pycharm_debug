# pycharm_debug
A module to connect a Python interpreter to a running 
[PyCharm remote debugging server](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config). 

Tested in DCC Applications;
- Maya
- Motionbuilder
- 3D Studio Max
- Blender
- Houdini
- Cascadeur


## Usage
1. Determine an available port number ie : **7520**
2. Start a remote debug configuration in PyCharm : [link](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config)
3. Run the following in the target Python interpreter :
```python
import pycharm_debug
pycharm_debug.start(port=7520)
# True
```

If the `pydevd` module is not yet discoverable for import, the latest PyCharm install is used instead.  
This convenience allows developers to frequently update PyCharm without needing to re-add the new install location for `pydevd`.


## Functions
### `pycharm_debug.start(port=7200, host='localhost')`


## Requirements
This module requires the `pydevd` module, which is part of the PyCharm installation.  
If not already available, it will attempt to automatically locate and import the 
appropriate `pydevd` module based on the installed PyCharm versions.


## Compatibility
This module has been tested on Windows. Support for other operating systems may be added in the future.


## License
This project is licensed under the [MIT License](LICENSE).


## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
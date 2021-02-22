.. ZonedRectangle:

**********************
Zoned Rectangles
**********************
This documents the contents, creation and access of the zoned rectangle library.
See :doc:`Examples/ZRectExample` for an example of how the :func:`gFunctionLibrary.coordinate_generator.ZonedRectangle`
class operates.

Contents
-----------
The following is a pseudo code for loop for the zoned rectangular fields currently in the
library.

.. code-block:: none

    For i = 4 To 28
        For j = i To 32
            Nx = i
            Ny = j
            Call ZonedRectangleGenerate(Nx, Ny)
        EndFor
    EndFor

The entire library is computed at B=5m spacing. The library took 254 days of computing time
using cpgfunctions adaptive discretization scheme.

Create Library File
---------------------
Here's an example of how to provide the path/to/output/ directory containing cpgfunction output files. The files are
merged into a single library.json file.

.. literalinclude:: ../gFunctionLibrary/Libraries/examples/output_to_library.py
    :language: python
    :linenos:


Library Access
--------------------------------
Provide functions for accessing the zoned rectangular library.
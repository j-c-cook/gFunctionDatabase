.. statistics:

****************************
Dimensioning Rules Example
****************************
A 7x10 borefield is chosen to verify the dimensioning rules of Eskilson and pygfunction.

Compute B/H Ratios
--------------------
To ensure that the g-function does scale with the dimensionless parameters, 5 g-functions varying different heights
are computed for borefields with uniform spacing of 5 and 8 meters. A table is created. The mean percentage errors
(computed with :py:meth:`gFunctionLibrary.statistics.mpe`) are presented in the table below.

.. raw:: html

    <embed>
    <style type="text/css">
    .tg {margin: 0 auto;}
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg .tg-baqh{text-align:center;vertical-align:top}
    .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
    </style>
    <body>
    <table class="center, tg">
    <caption>Mean percent errors for g-functions with the same B/H, and also computed using a separate B/H</caption>
    <thead>
      <tr>
        <th class="tg-c3ow">B</th>
        <th class="tg-c3ow">H<sub>0</sub><br></th>
        <th class="tg-c3ow">H<sub>1</sub></th>
        <th class="tg-baqh">H<sub>2</sub></th>
        <th class="tg-baqh">H<sub>3</sub></th>
        <th class="tg-baqh">H<sub>4</sub></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-c3ow">5<br></td>
        <td class="tg-c3ow">96<br></td>
        <td class="tg-c3ow">48</td>
        <td class="tg-baqh">24</td>
        <td class="tg-baqh">12</td>
        <td class="tg-baqh">8</td>
      </tr>
      <tr>
        <td class="tg-c3ow">20</td>
        <td class="tg-c3ow">384</td>
        <td class="tg-c3ow">192</td>
        <td class="tg-baqh">96</td>
        <td class="tg-baqh">48</td>
        <td class="tg-baqh">32</td>
      </tr>
      <tr>
        <td class="tg-c3ow"><span style="font-weight:bold">MPE (%)</span></td>
        <td class="tg-c3ow">4.028e-05<br></td>
        <td class="tg-c3ow">-8.7e-06</td>
        <td class="tg-baqh">5.5e-04</td>
        <td class="tg-baqh">1.381e-02</td>
        <td class="tg-baqh">-4.759e-02</td>
      </tr>
    </tbody>
    </table>
    </body>
    </embed>

The g-functions from the table above are plotted in the :numref:`dr_fig_1`. The g-functions computed for the
borefield with a uniform spacing, B=5m, are listed in the `B/H library` legend. This was done because
this is like what will be in the library. The g-functions computed using the uniform spacing, B=20m, are listed
in the `B/H Computed` legend. The g-functions which have the same `B/H` value for the 5m and 20m spacing fields
are computed with the same color. There are two additional g-function curves computed for a B/H=0.0625, which
will be used as reference for interpolation later on.

.. figure:: images/dimensioning_rules_figure_01.png
    :name: dr_fig_1
    :align: center

    g-Functions plotted with the same rb/H, D/H and borehole layout (7x10), but with
    varied B/H values

Interpolation
---------------
New g-functions are computed that will specifically have a B/H value of 0.0625 to compare the interpolation
using the `library` g-function curves of 5m versus where the actual computed values fall.

.. raw:: html

    <embed>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
    .tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
    </style>
    <table class="tg">
    <caption>Mean percentage error of interpolation for a B/H=0.0625 using different interpolation methods</caption>
    <thead>
      <tr>
        <th class="tg-c3ow"><span style="font-weight:bold">Interpolation Method</span></th>
        <th class="tg-7btt">MPE (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-c3ow">linear</td>
        <td class="tg-c3ow"> -0.30</td>
      </tr>
      <tr>
        <td class="tg-c3ow">quadratic<br></td>
        <td class="tg-c3ow">-0.05<br></td>
      </tr>
      <tr>
        <td class="tg-c3ow">cubic</td>
        <td class="tg-c3ow">-0.02<br></td>
      </tr>
    </tbody>
    </table>
    </embed>

An interpolated g-function (using `cubic interpolation`) is now plotted on an updated :numref:`dr_fig_2`.

.. figure:: images/dimensioning_rules_figure_02.png
    :name: dr_fig_2
    :align: center

    An interpolated g-function curve of B/H=0.0625 is interpolated for using g-functions computed with
    a uniform spacing of 5m and ranging heights

Source Code
--------------

.. literalinclude:: ../gFunctionLibrary/examples/dimensioning_rules.py
    :language: python
    :linenos:

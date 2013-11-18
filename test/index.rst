.. Yuml test documentation master file, created by
   sphinx-quickstart on Sat Nov 16 17:11:22 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Yuml test's documentation!
=====================================

Contents:

.. toctree::
   :maxdepth: 2

Yuml tests and samples
======================

.. yuml:: 
	:type: activity

	[User]


.. yuml:: 
	:style: plain 

	[User]


.. yuml:: 
	:style: plain 

	[Customer]->[Billing Address]


.. yuml:: 
	:direction: TD

	[note: You can stick notes on diagrams too!{bg:cornsilk}],[Customer]<>1-orders 0..*>[Order], [Order]++*-*>[LineItem], [Order]-1>[DeliveryMethod], [Order]*-*>[Product], [Category]<->[Product], [DeliveryMethod]^[National], [DeliveryMethod]^[International]

.. yuml::

    [Brewery]<>-*>[Equipment]
    [Equipment]-*>[Sensor]
    [Sensor]-1>[SamplingConfiguration]
    [Sensor]-1>[ConversionConfiguration]


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


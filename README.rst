
============================================
``my-ip``: Get your public IP address. Fast.
============================================

|Codacy Badge|
|Black Badge|

``my-ip`` is a simple CLI script, that finds out your public IP by asynchronously requesting multiple services.


.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/683afc5412064a7da45b9b50ccd79975
   :target: https://www.codacy.com/manual/lainiwa/my-ip?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lainiwa/my-ip&amp;utm_campaign=Badge_Grade
   :alt: Code quality

.. |Black Badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black



Installation and Usage
======================

``my-ip`` is a Python-only package `hosted on PyPI`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing it:

.. _hosted on PyPI: https://pypi.org/project/my_ip/

.. code-block:: console

   $ pip install my_ip

Now run it to get your public address!

.. code-block:: console

   $ mip
   2019-10-12 08:19:58.070 | INFO     | my_ip.console:cli:76 - Standard config not found. Creating new
   First run.
   Installing config to `/home/lain/.config/my_ip/config.toml`... Done!
   185.xxx.xxx.xxx

As you can see, the script installed the configuration script on the first run. The second run will be less verbose though:

.. code-block:: console

   $ mip
   185.xxx.xxx.xxx



Getting Help
============

Have a question? File a `new issue`_!

.. _new issue: https://github.com/lainiwa/my-ip/issues/new

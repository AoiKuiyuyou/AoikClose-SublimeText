#
import operator

from functools import partial

import sublime
import sublime_plugin


#
class AoikCloseCommand(sublime_plugin.ApplicationCommand):
    """
    Close views in various ways.
    """

    _MODE_V_ACTIVE = 'active'
    _MODE_V_ALL = 'all'
    _MODE_V_LEFT = 'left'
    _MODE_V_RIGHT = 'right'
    _MODE_V_OTHER = 'other'
    _MODE_V_S = (
        _MODE_V_ACTIVE,
        _MODE_V_ALL,
        _MODE_V_LEFT,
        _MODE_V_RIGHT,
        _MODE_V_OTHER,
    )

    def _get_active_window_and_view(self):
        """
        Used in both "self.run" and "self.is_enabled".
        """

        # Get the active window
        window = sublime.active_window()

        # 6EIWL
        if window is None:
            return None

        # Get the active view
        active_view = window.active_view()

        # 8SI03
        if active_view is None:
            return None

        # Get the group index and view index
        active_group_index, active_view_index = \
            window.get_view_index(active_view)

        # 9YSZM
        if active_group_index < 0 or active_view_index < 0:
            return None

        #
        return (window, active_view, active_group_index, active_view_index)

    def run(self, **args):
        """
        @param mode:
        - 'active': close the active view.
        - 'all': close all views.
        - 'left': close all views to the left.
        - 'right': close all views to the right.
        - 'other': close all but the active view.
        Default is 'active'.

        @param force: force closing unsaved views without asking.
        Default is False.
        """
        # Get the active window and active view
        tuple_obj = self._get_active_window_and_view()

        if tuple_obj is None:
            return

        window, active_view, active_group_index, active_view_index = tuple_obj

        # Ensured at 6EIWL, 8SI03 and 9YSZM
        assert window is not None
        assert active_view is not None
        assert active_group_index >= 0
        assert active_view_index >= 0

        # 5JGLT
        # Get argument "mode"
        mode = args.get('mode', self._MODE_V_ACTIVE)

        assert mode in self._MODE_V_S, \
            ("""Argument "mode"'s value "{}" is not one of {}.""")\
            .format(mode, self._MODE_V_S)

        # Get "decide_close" function according to argument "mode".
        # It takes a view index and returns True if the view should be closed.
        if mode == self._MODE_V_ACTIVE:
            decide_close = partial(operator.eq, active_view_index)
        elif mode == self._MODE_V_ALL:
            decide_close = (lambda x: True)
        elif mode == self._MODE_V_LEFT:
            decide_close = partial(operator.gt, active_view_index)
        elif mode == self._MODE_V_RIGHT:
            decide_close = partial(operator.lt, active_view_index)
        elif mode == self._MODE_V_OTHER:
            decide_close = partial(operator.ne, active_view_index)
        else:
            # Ensured at 5JGLT
            assert mode in self._MODE_V_S, repr(mode)

        # Get argument "force"
        force = args.get('force', False)

        # Get all views in the group
        view_s = window.views_in_group(active_group_index)

        # A list of views to close
        view_s_to_close = []

        # Start to collect the list of views to close
        for view_index, view in enumerate(view_s):
            # If the view should be closed
            if decide_close(view_index):
                # Add to the list
                view_s_to_close.append(view)

        # If force closing unsaved views without asking
        if force:
            for view in view_s_to_close:
                # Set to scratch.
                # Scratch views never report as being dirty.
                view.set_scratch(True)

        # Start to close the list of views
        for view in view_s_to_close:
            # Get the group index and view index.
            # "get_view_index" will return -1 if not found.
            group_index, view_index = window.get_view_index(view)

            # If the view exists
            if view_index >= 0:
                # Close the view
                window.run_command(
                    'close_by_index',
                    {'group': group_index, 'index': view_index}
                )

    def is_enabled(self):
        return self._get_active_window_and_view() is not None

    def is_visible(self):
        return True

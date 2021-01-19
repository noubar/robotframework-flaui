from enum import Enum
from FlaUILibrary.flaui.exception import FlaUiError
from FlaUILibrary.flaui.interface import ModuleInterface


class ListBox(ModuleInterface):
    """
    List control module wrapper for FlaUI usage.
    Wrapper module executes methods from ListBox.cs implementation.
    """

    class Action(Enum):
        """Supported actions for execute action implementation."""
        SELECT_LIST_CONTROL_ITEM_BY_INDEX = "SELECT_LIST_CONTROL_ITEM_BY_INDEX"
        LIST_CONTROL_SHOULD_CONTAIN = "LIST_CONTROL_SHOULD_CONTAIN"
        GET_LIST_CONTROL_ITEMS_COUNT = "GET_LIST_CONTROL_ITEMS_COUNT"
        GET_ALL_NAMES_FROM_SELECTED_ELEMENT = "GET_ALL_NAMES_FROM_SELECTED_ELEMENT"
        LIST_CONTROL_SHOULD_HAVE_SELECTED_ITEM = "LIST_CONTROL_SHOULD_HAVE_SELECTED_ITEM"
        GET_SELECTED_ITEMS_FROM_LIST_CONTROL = "GET_SELECTED_ITEMS_FROM_LIST_CONTROL"

    def execute_action(self, action, values=None):
        """If action is not supported an ActionNotSupported error will be raised.

        Supported actions for checkbox usages are:

          *  Action.SELECT_LIST_CONTROL_ITEM_BY_INDEX
            * values (Array): [Element, Number]
            * Returns : None

          *  Action.COMBOBOX_SHOULD_CONTAIN
            * values (Array): [Element, String]
            * Returns : None

          *  Action.GET_LIST_CONTROL_ITEMS_COUNT
            * values (Array): [Element]
            * Returns : None

        *  Action.GET_ALL_NAMES_FROM_SELECTED_ELEMENT
            * values (Array): [Element]
            * Returns : None

        *  Action.LIST_CONTROL_SHOULD_HAVE_SELECTED_ITEM
            * values (Array): [Element, String]
            * Returns : None

        *  Action.GET_SELECTED_ITEMS_FROM_LIST_CONTROL
            * values (Array): [Element]
            * Returns : String from all selected items.

        Raises:
            FlaUiError: If action is not supported.

        Args:
            action (Action): Action to use.
            values (Object): See action definitions for value usage.
        """
        switcher = {
            self.Action.SELECT_LIST_CONTROL_ITEM_BY_INDEX:
                lambda: ListBox._select_list_control_by_index(values[0], values[1]),
            self.Action.LIST_CONTROL_SHOULD_CONTAIN:
                lambda: ListBox._list_control_should_contain(values[0], values[1]),
            self.Action.GET_LIST_CONTROL_ITEMS_COUNT:
                lambda: values[0].Items.Length,
            self.Action.GET_ALL_NAMES_FROM_SELECTED_ELEMENT:
                lambda: ListBox._get_all_names_from_selected_element(values[0]),
            self.Action.LIST_CONTROL_SHOULD_HAVE_SELECTED_ITEM:
                lambda: ListBox._list_control_should_have_selected_item(values[0], values[1]),
            self.Action.GET_SELECTED_ITEMS_FROM_LIST_CONTROL:
                lambda: ListBox._get_selected_items(values[0])
        }

        return switcher.get(action, lambda: FlaUiError.raise_fla_ui_error(FlaUiError.ActionNotSupported))()

    @staticmethod
    def _get_selected_items(element):
        """Try to get all selected items as string.

        Args:
            element (Object): List view to select items.

        Returns:
            String from all selected items separated as pipe for example:
                Value 1
                Value 2
        """

        values = ""

        for selected_item in element.SelectedItems:
            values += selected_item.Text + "\n"

        return values

    @staticmethod
    def _select_list_control_by_index(element, index):
        """Try to select element from given index.

        Args:
            element (Object): List control UI object.
            index   (Number): Index number to select

        Raises:
            FlaUiError: By an array out of bound exception
            FlaUiError: If value is not a number.
        """
        try:
            element.Items[int(index)].Select()
        except IndexError:
            raise FlaUiError(FlaUiError.ArrayOutOfBoundException.format(index)) from None
        except ValueError:
            raise FlaUiError(FlaUiError.ValueShouldBeANumber.format(index)) from None

    @staticmethod
    def _list_control_should_have_selected_item(control, item):
        """Verification if item from list control is selected.

        Args:
            control (Object): List control UI object.
            item    (String): Item name which should be selected.

        Raises:
            FlaUiError: By an array out of bound exception
            FlaUiError: If value is not a number.
        """
        names = ListBox._get_all_names_from_selected_element(control)
        if item not in names:
            raise FlaUiError(FlaUiError.ItemNotSelected.format(item))

    @staticmethod
    def _get_all_names_from_selected_element(control):
        """Get all names from selected element.

        Args:
            control (Object): List control element from FlaUI.

        Returns:
            List from all names from list control if exists otherwise empty list.
        """
        names = []

        for selected_item in control.SelectedItems:
            names.append(selected_item.Name)

        return names

    @staticmethod
    def _list_control_should_contain(control, name):
        """Checks if Combobox contains an item.

        Args:
            control (Object): List control element from FlaUI.
            name (String): Name from combobox item which should exist.

        Returns:
            True if name from combobox item exists otherwise False.
        """
        for item in control.Items:
            if item.Name == name:
                return

        raise FlaUiError(FlaUiError.ControlDoesNotContainItem.format(name))
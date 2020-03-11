"""Author: Richard Hua
CPE 202: Lab 4 - OrderedList
"""
class Node:
    """ A node of a list
    Attributes:
        val (int): the payload
        next (Node): the next item in the list
        prev (Node): the previous item in the list
    """
    def __init__(self, val, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

    def __repr__(self):
        return "Node(val=%s, next=%s, prev=%s)"\
        % (self.val, self.next, self.prev)

    def __eq__(self, other):
        return (self.val == other.val) and\
        (self.next == other.next) and (self.prev == self.prev)

class OrderedList:
    """an ordered list
    Attributes:
        head (Node): a ponter to the head of the list
        tail (Node): a pointer to the tail of the list
        num_items (int): the number of items stored in the list
    """
    def __init__(self, head=None, tail=None, num_items=0):
        self.head = head
        self.tail = tail
        self.num_items = num_items

    def __eq__(self, other):
        return (self.head == other.head) and\
        (self.tail == other.tail) and (self.num_items == self.num_items)

    def __repr__(self):
        return "OrderedList(head=%s, tail=%s, num_items=%s)"\
        % (self.head, self.tail, self.num_items)

    def insert_before(self, node, item):
        """Helper: Create a Node(item) and insert to space between current node and prev node.
        Builds link from new node to previous node. Then connects next links to curr node.
        Args:
            node (Node): the current node to insert before
            item (int): the value to be inserted
        """
        new = Node(item)
        new.prev = node.prev
        node.prev = new
        new.next = node
        if new.prev is not None: # arbitrary point exists after node
            new.prev.next = new
        else: # Inserted to beginning of list. Set new head.
            self.head = new
            if node.next is None: #inserted to list of size=1 => old node is tail
                self.tail = node

    def insert_after(self, node, item):
        """Helper: Create a Node(item) and insert to space between current node and next node.
        Builds link from new node to current node and vice versa.
        Then connects new node to the next one pointed by curr node.
        Args:
            node (Node): the current node to insert after
            item (int): the value to be inserted
        """
        new = Node(item)
        new.next = node.next
        node.next = new
        new.prev = node
        if new.next is not None: # arbitrary point exists after node
            node.next.prev = new
        if new.next is None: # Inserted to EOL. Set new rear.
            self.tail = new

    def add_helper(self, node, item):
        """Helper function to add to linked list in ascending order (smallest to greatest).
        Args:
            node (Node): the node to start recursion from
            item (int): the value to be inserted
        """
        if node.val >= item:
            self.insert_before(node, item)
        elif node.next is None: # Recursed to end already, check edge cases
            if node.val >= item:
                self.insert_before(node, item)
            else: #  node.val <= item
                self.insert_after(node, item)
        else: #Recurse down list if not at end or val not added yet
            self.add_helper(node.next, item)

    def add(self, item):
        """adds a specified value as an item in the list while maintaining ascending order.
        Args:
            item (int): a value to be added as an item in the list
        """
        self.num_items += 1
        #Case 1: Empty list
        if self.head is None:
            self.head = Node(item)
            self.tail = self.head
        #Case 2: New smallest value, insert at beginning of list
        elif self.head.val >= item:
            self.insert_before(self.head, item)
        #Case 3: New largest value, insert at ending of list
        elif self.tail.val <= item:
            self.insert_after(self.tail, item)
        else:
        #Case 4: In the middle of list
            self.add_helper(self.head, item)

    def remove(self, item):
        """removes the first occurrence of a specified value in the list
        while maintaining ascending order.
        Args:
            item (int): a value to be removed
        Returns:
            int: the position where the item removed
        Raises:
            ValueError: when the item is not found in the list
        """
        pos = 0
        #Case 1 (Not in bounds): Empty list OR min > item > max
        if (self.head is None) or (self.tail.val < item) or (self.head.val > item):
            raise ValueError
        if self.head.val == item:
            return pos
        elif self.tail.val == item:
            return self.num_items
        else:
            return self.remove_helper(self.head, item, pos)

    def remove_helper(self, node, item, pos):
        """ Helper function to remove the first occurrence of a specified value
         in the list while maintaining ascending order.
        Args:
            node (Node): current Node
            item (int): a value to be removed
            pos (int): pos of the Node which holds item
        Returns:
            int: the position where the item removed
        Raises:
            ValueError: when the item is not found in the list
        """
        # print(type(node.val))
        if node.val == item:
            node.prev.next = node.next
            node.next.prev = node.prev
            node = None
            return pos
        if node.next is None:
            raise ValueError
        pos += 1
        return self.remove_helper(node.next, item, pos)

    def search_forward(self, item):
        """searches a specified item in the list starting from the head.
        Args:
            item (int): the value to be searched in the list
        Returns:
            bool: True if found, False otherwise.
        """
        if self.head is None:
            return False
        return self.search_forward_helper(self.head, item)

    def search_forward_helper(self, node, item):
        """Helper func that searches a specified item in the list starting from the head.
        Args:
            node (Node): head node of list to recurse forward
            item (int): the value to be searched in the list
        Returns:
            bool: True if found, False otherwise.
        """
        if node.val == item:
            return True
        if node.next is None:
            return False
        return self.search_forward_helper(node.next, item)

    def search_backward(self, item):
        """searches a specified item in the list backward starting from the tail.
        Args:
            item (int): the value to be searched in the list
        Returns:
            bool: True if found, False otherwise.
        """
        if self.tail is None:
            return False
        return self.search_backward_helper(self.tail, item)

    def search_backward_helper(self, node, item):
        """Helper func that searches a specified item in the list backward starting from the tail.
        Args:
            node (Node): head node of list to recurse backwards
            item (int): the value to be searched in the list
        Returns:
            bool: True if found, False otherwise.
        """
        if node.val == item:
            return True
        if node.prev is None:
            return False
        return self.search_backward_helper(node.prev, item)

    def is_empty(self):
        """checks if the list is empty.
        Returns:
            bool: True if it is empty, False otherwise.
        """
        if self.num_items:
            return False
        return True

    def size(self):
        """gets the number of items stored in the list.
        Returns:
            int: the number of items in the list.
        """
        return self.num_items

    def index(self, item):
        """gets the position of the first occurrence of a specified item in the list.
        Args:
            item (int): the value to be found
        Returns:
            int: the position in the list
        Raises:
            LookupError: if the value is not found in the list
        """
        return self.index_pos_helper(self.head, item)

    def index_pos_helper(self, node, item, pos=-1):
        """Helper: gets the position of the first occurrence of a specified item in the list.
        Args:
            node (Node): the node to beginning recursing down list
            item (int): the value to be found
            pos (int): the position of the value in list
        Returns:
            int: the position in the list
        Raises:
            LookupError: if the value is not found in the list
        """
        pos += 1
        if pos > self.num_items - 1: #shorts recursion if pos not possible
            raise LookupError
        if node.val == item:
            return pos
        # if node.next is None:
        #     raise LookupError
        return self.index_pos_helper(node.next, item, pos)

    def pop(self, pos=None):
        """removes the item at a specified position and returns its value.
        The last item in the list is removed if the argument is not passed.
        Args:
            pos (int): the position of the item to be removed. The default value is None
        Returns:
            int: the value of the item that is removed
        Raises:
            IndexError: if the position is out of bound
        """
        if self.head is None:
            raise IndexError
        if pos is None: # remove last item and ret val
            self.num_items -= 1
            val = self.tail.val
            if self.tail.prev is None:
                self.head = None
                self.tail = None
                return val
            self.tail.prev.next = None
            self.tail = self.tail.prev
            return val
        return self.pop_helper(self.head, pos)

    def pop_helper(self, node, pos, idx=0):
        """pop() helper: removes the item at a specified position and returns its value.
        The last item in the list is removed if the argument is not passed.
        Args:
            node (Node): the head node to start search at
            pos (int): the pos of the item to be removed. Default value is None
            idx (int): a counter for current position. Used to check position against pos of item to remove.
        Returns:
            int: the value of the item that is removed
        Raises:
            IndexError: if the position is out of bound
        """
        if idx > pos:
            raise IndexError
        if node is None:
            raise IndexError
        if idx == pos:
            val = node.val
            if node.prev is not None:
                node.next.prev = node.prev
                node.prev.next = node.next
            else:
                node.next.prev = None
                self.head = node.next
                node = None
            self.num_items -= 1
            return val
        return self.pop_helper(node.next, pos, idx+1)

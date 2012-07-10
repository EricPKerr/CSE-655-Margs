def prettyPrintTree(tree, depth=0,
                        indent_str='    ',
                        node_str='+',
                        leaf_str='',
                        vline_str='|'):
    """Recursively print a tree representation. A tree node is an tagged
    iterable and a tree leaf is anything that can be turn into a string.
    """
    # print the tag first
    indent = vline_str + indent_str
    print depth * indent + node_str + str(tree[0])
    depth += 1
    for e in tree[1:]:
        if _isInternalNode(e):
            prettyPrintTree(e, depth, indent_str, node_str, leaf_str, vline_str)
        else:
            print depth * indent + leaf_str + str(e)

def _isInternalNode(node):
    """Any iterable whose first element is a string (tagged) is considered an
    internal node. In this system this includes a non-leaf parse tree node, or
    an ASTNode instance who behaves like a list.
    """
    return node and hasattr(node, '__iter__') and isinstance(node[0], str)

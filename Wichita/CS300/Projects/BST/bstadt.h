#include "bstadt_impl.h"

BST_TREE *BST_Create (int (*compare_from_appl) (void *arg1, void *arg2));

bool BST_Insert(BST_TREE* tree, int* dataPtr);

void* BST_Retrieve  (BST_TREE* tree, void* dataPtr);

bool BST_Delete (BST_TREE* tree, void* deleteNode);

void BST_Destroy (BST_TREE* tree);

void breadth_Traversal(NODE* ptr);

void inorder_Traversal(NODE* ptr);


// CONSTANTS
#define EMPTY 0			//_
#define CHANCELLOR 1	//c
#define TAKEN 2			//-
#define CHILD 3			//o
#define INCEST 4		//x
#define TRUE 1			
#define FALSE 0		

// LIBRARIES 
#include <stdio.h>
#include <stdlib.h>

// USER-DEFINED STRUCTURES
typedef struct puzzle_node{
    int N;
    int hasSpace;
    int ** board; //2d array
}PUZZLE;

void initialize_btm(PUZZLE **** btm, int n){
	int i;

	(*btm) = (PUZZLE ***) malloc(sizeof(PUZZLE **)*n);
	for(i=0;i<n;i++){
		(*btm)[i] = (PUZZLE **) malloc(sizeof(PUZZLE *)*n);
	}

}

void initialize_puzzle_node(PUZZLE ** init_config, int n){
	int i,j;

	// initialize node
	(*init_config) = (PUZZLE*) malloc(sizeof(PUZZLE));
	(*init_config)->N = n;
	(*init_config)->hasSpace = TRUE;
		// initialize config
	(*init_config)->board = (int **) malloc(sizeof(int *)*n);
	for(i=0;i<n;i++){
		(*init_config)->board[i] = (int *) malloc(sizeof(int)*n);
	}

	for (i=0;i<n;i++){
		for (j=0;j<n;j++){
			(*init_config)->board[i][j] = EMPTY;
		}
	}
}

// given x, y as coordinates of C, fill up vulnerable spaces of board
void fill_taken(PUZZLE * puzzle_node, int x, int y){
	int n = puzzle_node->N;
	int i,j;
	// horizontal dashes
	for(j=0;j<n;j++){
		if(puzzle_node->board[x][j] == EMPTY)
			puzzle_node->board[x][j] = TAKEN;
	}
	// vertical dashes
	for(i=0;i<n;i++){
		if(puzzle_node->board[i][y] == EMPTY)
			puzzle_node->board[i][y] = TAKEN;
	}
	// knight movement
	if(x-1>=0 && y-2>=0 && puzzle_node->board[x-1][y-2] == EMPTY)
		puzzle_node->board[x-1][y-2] = TAKEN;
	if(x-2>=0 && y-1>=0 && puzzle_node->board[x-2][y-1] == EMPTY)
		puzzle_node->board[x-2][y-1] = TAKEN;
	if(x+1<n && y+2<n && puzzle_node->board[x+1][y+2] == EMPTY)
		puzzle_node->board[x+1][y+2] = TAKEN;
	if(x+2<n && y+1<n && puzzle_node->board[x+2][y+1] == EMPTY)
		puzzle_node->board[x+2][y+1] = TAKEN;
	if(x-1>=0 && y+2<n && puzzle_node->board[x-1][y+2] == EMPTY)
		puzzle_node->board[x-1][y+2] = TAKEN;
	if(x-2>=0 && y+1<n && puzzle_node->board[x-2][y+1] == EMPTY)
		puzzle_node->board[x-2][y+1] = TAKEN;
	if(x+1<n && y-2>=0 && puzzle_node->board[x+1][y-2] == EMPTY)
		puzzle_node->board[x+1][y-2] = TAKEN;
	if(x+2<n && y-1>=0 && puzzle_node->board[x+2][y-1] == EMPTY)
		puzzle_node->board[x+2][y-1] = TAKEN;

}

void checkif_hasSpace(PUZZLE * parent){
	int i,j;
	int n = parent->N;

	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			if(parent->board[i][j] == EMPTY)
				return;
		}
	}

	parent->hasSpace = FALSE;
}

void print_puzzle_node(PUZZLE * node){
	int i,j,cell;

	for(i=0;i<node->N;i++){
		for(j=0;j<node->N;j++){
			cell = node->board[i][j];
			if(cell == EMPTY)
				printf("_ ");
			if(cell == CHANCELLOR)
				printf("C ");
			if(cell == TAKEN)
				printf("- ");
			if(cell == CHILD)
				printf("o ");
			if(cell == INCEST)
				printf("x ");
		}
		printf("\n");
	}
}

void populate(PUZZLE *parent, PUZZLE ***btm, int * nsiblings, int curr_stack){
	int i,j;
	int n = parent->N;
	int firstSpacei = -1;
	int firstSpacej = -1;
	PUZZLE * new_puzzle_ptr; // child

	while (parent->hasSpace){
		//make_anak
		initialize_puzzle_node(&new_puzzle_ptr, n); // create node
		for(i=0;i<n;i++){
			for(j=0;j<n;j++){
				// finding coordinates of first empty space
				if(firstSpacei == -1 && parent->board[i][j] == EMPTY){
					firstSpacei = i;
					firstSpacej = j;
				}
				// copy C's and -'s of parent to child
				if(parent->board[i][j] == CHANCELLOR)
					new_puzzle_ptr->board[i][j] = CHANCELLOR;
				else if(parent->board[i][j] == TAKEN)
					new_puzzle_ptr->board[i][j] = TAKEN;
			}
		}
		// update parent and child boards
		new_puzzle_ptr->board[firstSpacei][firstSpacej] = CHANCELLOR;
		parent->board[firstSpacei][firstSpacej] = CHILD;
		fill_taken(new_puzzle_ptr, firstSpacei, firstSpacej);
		// update parent according to incest rule
		for(i=0;i<n;i++){
			for(j=0;j<n;j++){
				if(new_puzzle_ptr->board[i][j] == EMPTY)
					parent->board[i][j] = INCEST;
			}
		}

		// connect new child to btm
		btm[curr_stack][nsiblings[curr_stack]] = new_puzzle_ptr;
		// update stack pointers
		nsiblings[curr_stack]++;
		// reset first free coordinates
		firstSpacei = -1;
		checkif_hasSpace(parent);
		checkif_hasSpace(new_puzzle_ptr);
	}
}

void initialize_nsiblings(int ** nsiblings, int n){
	int i;
	// instantiate
	(*nsiblings) = (int *) malloc(sizeof(int)*n);
	// initialize values
	for(i=0;i<n;i++){
		(*nsiblings)[i] = 0;
	}
}

void print_btm(int n, PUZZLE *** btm, int * nsiblings, int curr_node, int curr_stack){
	int layer, i, j, sib;
	int cell;

	printf("\nBacktracking Matrix\n");

	// for each layer
	for(layer=0;layer<curr_stack+1;layer++){
		// line break
		for(i=0;i<n*(n+1)*2;i++){
			printf("-");
		}
		printf(" %d", nsiblings[layer]);
		printf("\n");
		// for each row of whole layer
		for(i=0;i<n;i++){
			// for each cases in that layer
			for(sib=0;sib<nsiblings[layer]; sib++){
				// for each cell across all cases
				for(j=0;j<n;j++){
					// printf("btm[%d][%d]->board[%d][%d]\n", layer, sib, i, j);
					cell = btm[layer][sib]->board[i][j];
					switch(cell){
						case EMPTY:
							printf("  ");
							break;
						case CHANCELLOR:
							printf("C ");
							break;
						case TAKEN:
							printf("- ");
							break;
						case CHILD:
							printf("o ");
							break;
						case INCEST:
							printf("x ");
							break;
					}
				}
				printf("| ");
			}
			printf("\n");
		}
	}
	for(i=0;i<n*(n+1)*2;i++){
		printf("-");
	}
	printf("\n");

}

void print_nsiblings(int * nsiblings, int n){
	int layer;

	printf(" ___ \n");
	for(layer=0;layer<n;layer++){
		printf("| %d |\n", nsiblings[layer]);
	}
	printf(" --- \n");
}

int main(){
	// VARIABLES 
	int start = 0;
	int curr_stack = 0;
	int curr_node = 0;
	int n = 4;
	PUZZLE * init_config;
	PUZZLE *** btm; //backtracking matrix (2d array of pointers)4
	int * nsiblings;

	initialize_puzzle_node(&init_config, n);
	initialize_nsiblings(&nsiblings, n);
	initialize_btm(&btm,n);
	populate(init_config,btm,nsiblings,curr_stack);

	while(nsiblings[start] > 0){
		curr_node = nsiblings[curr_stack]-1;
		print_btm(n, btm, nsiblings, nsiblings[curr_stack]-1, curr_stack);
		// pushing
		if (btm[curr_stack][curr_node]->hasSpace){
			populate(btm[curr_stack][curr_node], btm, nsiblings, curr_stack+1);
			curr_stack++;
		}
		// popping
		else{
			//solution found! pop up
			if(curr_stack == n-1){ 
				printf("SOLUTION FOUND\n");
				print_puzzle_node(btm[curr_stack][curr_node]);
				// pop up
				nsiblings[curr_stack]--;
				curr_stack--;
			}
			//may sibling, pop side
			else if(nsiblings[curr_stack] > 1) {
				nsiblings[curr_stack]--;
			}
			// no more sibling aka dead end, pop up
			else if(nsiblings[curr_stack] == 1){
				nsiblings[curr_stack]--;
				curr_stack--;
			}
		}
	}



	return 0;
}
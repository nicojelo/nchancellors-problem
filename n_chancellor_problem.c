// CONSTANTS
#define EMPTY '0'			//_
#define CHANCELLOR '1'	//c
#define TAKEN 2			//-
#define CHILD 3			//o
#define INCEST 4		//x
#define TRUE 1			
#define FALSE 0		

// LIBRARIES 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// USER-DEFINED STRUCTURES
typedef struct puzzle_node{
    int N;
    int hasSpace;
    int ** board; //2d array
    int numCs;
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
	(*init_config)->numCs = 0;
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
		// count number of chancellors in new puzzle node
		new_puzzle_ptr->numCs = parent->numCs+1;
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

void free_puzzle_node(PUZZLE * puzzle_node){
	int i,j;
	int n = puzzle_node->N;

	for(i=0;i<n;i++){
		free(puzzle_node->board[i]);
	}
	free(puzzle_node->board);
}

void free_btm(PUZZLE *** btm, int n){
	int i,j,k;

	for(i=0; i<n; i++){
		for(j=0; j<n; j++){
			if(btm[i][j] != NULL)
				free(btm[i][j]);
		}
		if(btm[i] != NULL)
			free(btm[i]);
	}
	if(btm != NULL)
		free(btm);
}

void chancy(PUZZLE * init_config){
	int start = 0;
	int curr_stack = 0;
	int curr_node = 0;
	int n = init_config->N;
	PUZZLE *** btm; //backtracking matrix (2d array of pointers)4
	int * nsiblings;
	int num_solutions = 0;

	initialize_nsiblings(&nsiblings, n);
	initialize_btm(&btm,n);
	populate(init_config,btm,nsiblings,curr_stack);

	// print_puzzle_node(init_config);
	// print_btm(n, btm, nsiblings, nsiblings[curr_stack]-1, curr_stack);

	while(nsiblings[start] > 0){
		curr_node = nsiblings[curr_stack]-1;
		// print_btm(n, btm, nsiblings, nsiblings[curr_stack]-1, curr_stack);
		// pushing
		if (btm[curr_stack][curr_node]->hasSpace){
			populate(btm[curr_stack][curr_node], btm, nsiblings, curr_stack+1);
			curr_stack++;
		}
		// popping
		else{
			//solution found! pop up
			if(btm[curr_stack][curr_node]->numCs == n){ 
				// printf("SOLUTION FOUND\n");
				// print_puzzle_node(btm[curr_stack][curr_node]);
				free_puzzle_node(btm[curr_stack][curr_node]);
				// pop up
				nsiblings[curr_stack]--;
				curr_stack--;
				num_solutions++;
			}
			//may sibling, pop side
			else if(nsiblings[curr_stack] > 1) {
				free_puzzle_node(btm[curr_stack][curr_node]);
				nsiblings[curr_stack]--;
			}
			// no more sibling aka dead end, pop up
			else if(nsiblings[curr_stack] == 1){
				// printf("DEADEND BOI\n");
				// print_puzzle_node(btm[curr_stack][curr_node]);
				free_puzzle_node(btm[curr_stack][curr_node]);
				nsiblings[curr_stack]--;
				curr_stack--;
			}
		}
	}

	free(nsiblings);
	// free_btm(btm, n);
	printf("Number of solutions: %d\n", num_solutions);
}

int is_valid_config(PUZZLE * puzzle_node){
	int n = puzzle_node->N;
	int i,j, k,l, cell;

	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			cell = puzzle_node->board[i][j];
			if(cell == CHANCELLOR){
				// horizontal dashes
				for(k=0;k<n;k++){
					if(k!=j && puzzle_node->board[i][k] == CHANCELLOR)
						return FALSE;
				}
				// vertical dashes
				for(k=0;k<n;k++){
					if(i!=k && puzzle_node->board[k][j] == CHANCELLOR)
						return FALSE;
				}

				// knight movement
				if(i-1>=0 && j-2>=0 && puzzle_node->board[i-1][j-2] == CHANCELLOR)
					return FALSE;
				if(i-2>=0 && j-1>=0 && puzzle_node->board[i-2][j-1] == CHANCELLOR)
					return FALSE;
				if(i+1<n && j+2<n && puzzle_node->board[i+1][j+2] == CHANCELLOR)
					return FALSE;
				if(i+2<n && j+1<n && puzzle_node->board[i+2][j+1] == CHANCELLOR)
					return FALSE;
				if(i-1>=0 && j+2<n && puzzle_node->board[i-1][j+2] == CHANCELLOR)
					return FALSE;
				if(i-2>=0 && j+1<n && puzzle_node->board[i-2][j+1] == CHANCELLOR)
					return FALSE;
				if(i+1<n && j-2>=0 && puzzle_node->board[i+1][j-2] == CHANCELLOR)
					return FALSE;
				if(i+2<n && j-1>=0 && puzzle_node->board[i+2][j-1] == CHANCELLOR)
					return FALSE;
			}
		}
	}

	return TRUE;

	
}

void fill_taken_board(PUZZLE * puzzle_node){
	int i,j;
	int n = puzzle_node->N;

	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			if(puzzle_node->board[i][j] == CHANCELLOR){
				fill_taken(puzzle_node, i, j);
				puzzle_node->numCs++;	
			}
		}
	}
}

int main(){
	FILE *fp;
	int N,i,j,k,n;
	char *row;
	PUZZLE * init_config;

	fp = fopen("input.txt","r"); //opens the file
	fscanf(fp,"%d",&N);
	// iterate over all init_configs
	for(i=0;i<N;i++){
		fscanf(fp,"%d",&n);
		initialize_puzzle_node(&init_config, n);
		fgetc(fp);
		// iterate rows of current init_config
		for(j=0;j<n;j++){
			fgets(row,n+2,fp);
			row[strlen(row)-1] = '\0';
			for(k=0;k<n;k++){
				init_config->board[j][k] = row[k];
			}
		}

		if(is_valid_config(init_config)){
			fill_taken_board(init_config);
			chancy(init_config);
		}
		else{
			printf("Initial board is invalid :<\n");
		}
	}
	return 0;
}
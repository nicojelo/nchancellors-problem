#define EMPTY 0			//space
#define CHANCELLOR 1		//c
#define TAKEN 2			//-
#define CHILD 3			//o
#define INCEST 4			//x
#define TRUE 1			
#define FALSE 0			
#include <stdio.h>
#include <stdlib.h>



typedef struct puzzle{
    int N;
    int hasSpace;
    int ** config; //2d array

}PUZZLE;

void initialize_btm(PUZZLE *** btm,int n){
	int i;

	(*btm) = (PUZZLE **) malloc(sizeof(PUZZLE *)*n);
	for(i=0;i<n;i++){
		(*btm)[i] = (PUZZLE *) malloc(sizeof(PUZZLE)*n);
	}

}

void initialize_puzzle(PUZZLE ** init_config, int n){
	int i,j;

	// initialize node
	(*init_config) = (PUZZLE*) malloc(sizeof(PUZZLE));
	(*init_config)->N = n;
	(*init_config)->hasSpace = FALSE;
		// initialize config
	(*init_config)->config = (int **) malloc(sizeof(int *)*n);
	for(i=0;i<n;i++){
		(*init_config)->config[i] = (int *) malloc(sizeof(int)*n);
	}

	for (i=0;i<n;i++){
		for (j=0;j<n;j++){
			(*init_config)->config[i][j] = EMPTY;
		}
	}
}

void populate(PUZZLE *parent, PUZZLE **btm, int * nsiblings, int * curr_stack, int * curr_node){
	int i,j;
	int n = parent->N;
	int firstSpacei = -1;
	int firstSpacej = -1;
	// btm[*curr_stack][*curr_node] iS JUST ANAK

	while (parent->hasSpace){
		//make_anak
		btm[*curr_stack][*curr_node] = (PUZZLE *) malloc(sizeof(PUZZLE));
		initialize_puzzle(&btm[curr_stack][curr_node], n);
		for(i=0;i<n;i++){
			for(j=0;j<n;j++){	
				if(parent->config[i][j] == CHANCELLOR)
					btm[*curr_stack][*curr_node]->config[i][j] = CHANCELLOR;
				else if(parent->config[i][j] == TAKEN)
					btm[*curr_stack][*curr_node]->config[i][j] = TAKEN;
				else if(firstSpacei == -1 && parent->config[i][j] == EMPTY)
					firstSpacei = i;
					firstSpacej = j;
			}
		}
		btm[*curr_stack][*curr_node]->config[firstSpacei][firstSpacej] = CHANCELLOR;
		parent->config[firstSpacei][firstSpacej] = CHILD;

	}
}

void print_puzzle_node(PUZZLE * node){
	int i,j,cell;

	for(i=0;i<node->N;i++){
		for(j=0;j<node->N;j++){
			cell = node->config[i][j];
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


int main(){
	// int num_p;
	// puzzle_container [num_p];

	//VARIABLES 

	int start = 0;
	int curr_stack = 0;
	int curr_node = 0;
	int n = 4;
	PUZZLE * init_config;
	PUZZLE ** btm; //backtracking matrix
	int nsiblings[n];

	initialize_puzzle(&init_config, n);
	print_puzzle_node(init_config);

	initialize_btm(&btm,n);
	populate(init_config,btm,&nsiblings,&curr_stack,&curr_node);
	print_puzzle_node(btm[0][0]);

	return 0;
}

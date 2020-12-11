// Game.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include "LinkedList.h"

class Node {
public:
	LIST_ENTRY listEntry;
	ULONG value;

	Node(ULONG value) {
		this->value = value;
	}

	Node* next() {
		return CONTAINING_RECORD(this->listEntry.Flink, Node, listEntry);
	}

	Node* prev() {
		return CONTAINING_RECORD(this->listEntry.Blink, Node, listEntry);
	}

	ULONG Remove() {
		ULONG value = this->value;
		RemoveEntryList(&this->listEntry);
		delete this;

		return value;
	}

	Node* AddAfter(ULONG value) {
		Node* newNode = new Node(value);

		InsertHeadList(&this->listEntry, &newNode->listEntry);

		return newNode;
	}
};


ULONG* play(ULONG players, ULONG maxPoints)
{
	ULONG* scores = new ULONG[players];

	memset(scores, 0, sizeof(ULONG) * players);

	Node* origin = new Node(0);
	InitializeListHead(&origin->listEntry);

	Node* cur = origin;

	ULONG scoreIdx = 1;
	ULONG playerIdx = 1;
	for (ULONG turn = 1; turn <= maxPoints; ++turn, ++scoreIdx, ++playerIdx)
	{
		if (playerIdx == players) {
			playerIdx = 0;
		}
		if (scoreIdx == 23) {
			scoreIdx = 0;

			cur = cur->prev()->prev()->prev()->prev()->prev()->prev();
			scores[playerIdx] += turn + cur->prev()->Remove();
		}
		else {
			cur = cur->next()->AddAfter(turn);
		}
	}

	return scores;
}

int main(int argc, const char** argv)
{
	if (argc < 3) {
		std::cout << "Usage: ./" << argv[0] << " num_players max_points\n";
	}

	ULONG players = strtoul(argv[1], NULL, 0);
	ULONG maxPoints = strtoul(argv[2], NULL, 0);

	ULONG* scores = play(players, maxPoints);

	ULONG maxScore = 0;
	for (ULONG p = 0; p < players; ++p) {
		if (scores[p] > maxScore) {
			maxScore = scores[p];
		}
	}

	std::cout << "Best Score: " << maxScore;

	return 0;
}


// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file

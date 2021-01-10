#pragma once
#include "queue.hpp"

class QueueLinkedList : public Queue
{
    struct Node // struct can be defined internally to avoid exposing internals
    {
        int value;
        Node *next;
    };

public:
    void enqueue(int value);
    int dequeue();
    bool empty() const;
    bool full() const;

private:
    Node **ll;
};
#pragma once
#include "queue.hpp"

class QueueArray : public Queue
{
public:
    void enqueue(int value);
    int dequeue();
    bool empty() const;
    bool full() const;

private:
    int array[100];
};
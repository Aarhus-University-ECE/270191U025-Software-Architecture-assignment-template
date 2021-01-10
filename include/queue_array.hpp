#pragma once

class QueueArray
{
public:
    void enqueue(int value);
    int dequeue();
    bool empty() const;
    bool full() const;

private:
    int array[100];
};
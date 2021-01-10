#pragma once

class Queue
{
public:
    virtual void enqueue(int value) = 0;
    virtual int dequeue() = 0;
    virtual bool empty() const = 0;
    virtual bool full() const = 0;
};
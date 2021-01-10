#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"
#include "queue_array.hpp"
#include "queue_linked_list.hpp"
#include "queue.hpp"

// See Catch2's documentation: https://github.com/catchorg/Catch2/blob/devel/docs/tutorial.md#scaling-up
TEST_CASE("QueueArray")
{
    QueueArray q;

    SECTION("Queue starts empty")
    {

        REQUIRE(q.empty() == true);
    }

    SECTION("enqueue then dequeue")
    {
        q.enqueue(1);
        REQUIRE(q.empty() != true);
        REQUIRE(q.dequeue() == 1);
        REQUIRE(q.empty() == true);
    }
}

TEST_CASE("QueueLinkedList")
{
    QueueLinkedList q;

    SECTION("Queue starts empty")
    {

        REQUIRE(q.empty() == true);
    }

    SECTION("enqueue then dequeue")
    {
        q.enqueue(1);
        REQUIRE(q.empty() != true);
        REQUIRE(q.dequeue() == 1);
        REQUIRE(q.empty() == true);
    }
}

TEST_CASE("Queues accessed as abstract class")
{
    Queue *q = GENERATE(new QueueArray(), new QueueLinkedList());

    SECTION("Queue starts empty")
    {

        REQUIRE(q->empty() == true);
    }

    SECTION("enqueue then dequeue")
    {
        q->enqueue(1);
        REQUIRE(q->empty() != true);
        REQUIRE(q->dequeue() == 1);
        REQUIRE(q->empty() == true);
    }

    delete q;
}

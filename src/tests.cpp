#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"
#include "queue_array.hpp"

// See Catch2's documentation: https://github.com/catchorg/Catch2/blob/devel/docs/tutorial.md#scaling-up

TEST_CASE("Queue starts empty", "[queue]")
{
    QueueArray q;

    REQUIRE(q.empty() == true);
}

TEST_CASE("enqueue then dequeue", "[queue]")
{
    QueueArray q;
    q.enqueue(0);
    REQUIRE(q.empty() != true);
    REQUIRE(q.dequeue() == 0);
    REQUIRE(q.empty() == true);
}

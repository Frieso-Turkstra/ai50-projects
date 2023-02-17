I started with a neural network similar to the one in the lecture, resulting in 5% accuracy.

I then added another hidden layer which did not improve anything.
So instead, I doubled the max-pooling layer which also did not increase the accuracy.

In the tensorflow guidelines, I saw that they used two convolutional layers followed by a max-pooling layer.
This dramatically improved the accuracy up to 97.8%.

Next, I wanted to see what would happen if I set the drop out to 0 (was 0.5).
In the training session, it reached 99% but its final score was 96% so there may have been some overfitting.

I dedided to try the same technique of two convolutional layers + 1 max-pooling layer again.
So now I had two convolutional layers, one max-pooling, two convolutional layers again and another max-pooling.
This resulted in a 97.6% accuracy so not much of a difference.

Lastly, I fiddled around with:
- the pool-size (from 2x2 to 3x3),
- the number of filters (from 32 to 50),
- and the number of neurons in the hidden layer (from 128 to 200).
But these changes did not do much either; final accuracy was 96.7%

Hence, I undid the last couple of changes and stuck with the first design which had 97.8% accuracy.

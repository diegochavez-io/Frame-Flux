# Set your parameters here
image_count = 110            # Number of images you have 
num_repeats = 2             # How many times each image is repeated
train_batch_size = 1        # Batch size for training
epochs = 20                # Desired number of epochs
target_total_steps = 2500   # Your target for total steps

def check_and_suggest_parameters(image_count, num_repeats, train_batch_size, epochs, target_total_steps):
    # Calculate steps per epoch and total steps
    steps_per_epoch = (image_count * num_repeats) / train_batch_size
    total_steps = steps_per_epoch * epochs
    
    print(f"With the given parameters:")
    print(f"- Images: {image_count}")
    print(f"- num_repeats: {num_repeats}")
    print(f"- train_batch_size: {train_batch_size}")
    print(f"- Epochs: {epochs}")
    print(f"You will achieve {total_steps:.0f} total steps, with each epoch having {steps_per_epoch:.2f} steps.")

    # Check if total steps meet the target
    if total_steps < target_total_steps:
        additional_epochs_needed = (target_total_steps - total_steps) / steps_per_epoch
        suggested_epochs = epochs + additional_epochs_needed
        print(f"To reach your target of {target_total_steps} total steps, consider increasing your epochs to {suggested_epochs:.0f}.")
    elif total_steps > target_total_steps:
        reduced_epochs_needed = epochs - (total_steps - target_total_steps) / steps_per_epoch
        suggested_epochs = max(1, reduced_epochs_needed)
        print(f"To reach closer to your target of {target_total_steps} total steps, consider reducing your epochs to {suggested_epochs:.0f}.")
    else:
        print("Your current setup perfectly matches the target total steps.")

# Call the function with your parameters
check_and_suggest_parameters(image_count, num_repeats, train_batch_size, epochs, target_total_steps)

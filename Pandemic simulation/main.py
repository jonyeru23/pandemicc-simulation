from simulation import *

def main():
    limits = (700, 500)
    num_blobs_healthy = 100
    num_infected_blobs = 10

    factory = BlobFactory()

    blobs = [factory.get_random_healthy_blob(limits) for _ in range(num_blobs_healthy)]
    infected_blobs = [factory.get_random_infected_blob(limits) for _ in range(num_infected_blobs)]

    blobs.extend(infected_blobs)

    board = Board(limits[0], limits[1])
    board.set_up()
    timer = 0
    while board.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.terminate()

        if timer > 100000:
            board.terminate()

        board.fill()

        for this_blob in blobs:
            for other_blob in blobs:
                if this_blob is other_blob:
                    continue

                this_blob.collision(other_blob)
            this_blob.move_and_age()
            board.draw(this_blob)

        pygame.display.update()
        timer += 1

    pygame.quit()









if __name__ == '__main__':
    main()
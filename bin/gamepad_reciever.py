import inputs


for i in dir(inputs):
	print(i)


def main():
	while True:
		events = inputs.get_gamepad()
		for event in events:
			print(event)


if __name__ == "__main__":
    main()

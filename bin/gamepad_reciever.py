
import time
import inputs


def parse_event(event):

    if event.code == "SYN_REPORT":
        return

    key = event.code
    val = event.state
    print(key,val)


def main():

    while True:


        print(inputs.devices.gamepads)

        try:
            events = inputs.get_gamepad()
            for event in events:
                parse_event(event)
        except OSError as e:
            print("oserror, trying to reinitialise controller")
            time.sleep(0.5)

            
            for i in dir(inputs):
                print(i)
            exit()



        except Exception as e:
            print(e)
            print(e.__class__.__name__)

            for i in dir(e):
                print(i)

            exit()




if __name__ == "__main__":
    main()
    pass

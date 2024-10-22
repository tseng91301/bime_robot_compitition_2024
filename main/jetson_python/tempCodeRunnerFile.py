while True:
    frame = recognition.get_frame()
    color = goose_weight.color_block_detect(frame)
    print(f"Color: {color}")

    if color == goose_weight.COLOR_BLUE:
        pass

    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
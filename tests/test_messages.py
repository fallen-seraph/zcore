import tests.windows_config_setup as wcs

def test_default_message():
    messageBuilder = messages.MessageHandler(None)
    assert "a scheduled reboot" == messageBuilder.message
    messageBuilder = messages.MessageHandler("this is a test")
    assert "this is a test" == messageBuilder.message

def test_reboot_time_message():
    messageBuilder = messages.MessageHandler(None)
    assert "Restarting the server for a scheduled reboot at <t:test:t>" == messageBuilder.reboot_time_message("test")
    messageBuilder = messages.MessageHandler("this is a test")
    assert "Restarting the server for this is a test at <t:test:t>" == messageBuilder.reboot_time_message("test")

def test_interval_message():
    messageBuilder = messages.MessageHandler(None)
    assert "Restarting the server for a scheduled reboot in 5 minutes." == messageBuilder.interval_message(5)
    messageBuilder = messages.MessageHandler("this is a test")
    assert "Restarting the server for this is a test in 5 minutes." == messageBuilder.interval_message(5)

def test_one_minute_message():
    messageBuilder = messages.MessageHandler(None)
    assert "Restarting the server for a scheduled reboot in 1 minute." == messageBuilder.one_minute_message()
    messageBuilder = messages.MessageHandler("this is a test")
    assert "Restarting the server for this is a test in 1 minute." == messageBuilder.one_minute_message()

if __name__ == '__main__':
    wcs.windows_config_builder()
    wcs.zcore_config_copy()
    from tools import messages
    test_default_message()
    test_reboot_time_message()
    test_interval_message()
    test_one_minute_message()
    wcs.windows_config_cleanup()
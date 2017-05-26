536	+    if [ -z "$VRIT_DRIVER" ]; then
537	+        # If there is not virt driver defined we assume nova is not installed
538	+        iniset $TEMPEST_CONFIG service_available nova "False"
539	+    fi
540	+

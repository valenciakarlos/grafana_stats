TPUT_and_Packet_Drops.pyread -p "Entre value" variable
echo "Variable is $variable"

echo "Entering the while"
line=""
while IFS= read -p "Enter Value (-1 to quit):" -r line
do
  echo "You typed: $line"
  if [ $line -eq -1 ]
  then
	  break
  fi
  echo "Processing $line"
done

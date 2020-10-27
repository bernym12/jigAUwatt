import matplotlib.pyplot as plt
import yaml
from sys import argv

def percent_diff(x,y):
    return [abs(float(((x-y)/x)))*100 for x,y in zip(x,y)]

def create_subplot(data, devices,x_axis, y_label,title, pos, ax_label):
    sub = plt.plot(pos, label=ax_label,title=title, ylabel=y_label, xlabel='Device', 
                    xticks=x_axis, xticklabels=devices)
    sub.scatter(x_axis, data)
    plt.xticks(fontsize=5)

'''
takes yaml file of power data and converts it into 
a power factor list, shelly list, and multimeter list
all contained in a data dict. 
Also gets a list of all of the devices.

@return data - Dictionary of wattmeter stats
@return devices - list of device names
'''
def file_processing(yaml_file):
    device_dict = yaml.safe_load(open(yaml_file, 'r'))
    data = dict()
    devices = device_dict.keys()
    for device in device_dict:
        for item in device_dict[device]:
            if item not in data:
                data[item] = list()
            data[item].append(device_dict[device][item])
    return data, devices

def main():
    data, devices = file_processing(argv[1])
    pf_times_shelly = [s*pf for s,pf in zip(data['shelly'], data['pf'])]
    shelly = percent_diff(data['multimeter'], pf_times_shelly)
    
    x_axis = [x for x in range(len(devices))]
    multimeter_vs_shelly = percent_diff(data['multimeter'], data['shelly'])
    plt.figure(figsize=(15,5))
    plt.scatter(x_axis, multimeter_vs_shelly, label='multimeter vs shelly')
    plt.scatter(x_axis, shelly, label='multimeter vs pf*shelly')
    ax = plt.gca()
    # create_subplot(multimeter_vs_shelly, devices, x_axis,'Percent Difference', "Sonoff vs Multimeter Percent Current Diff", 211, 'Son')
    plt.legend(loc="upper left")
    plt.xticks(x_axis)
    ax.set_xticklabels(devices)
    plt.xticks(fontsize=6)

    plt.title('Percent Difference in Current Readings')
    plt.ylabel('Percent Difference')

    # create_subplot(multimeter_vs_pf, devices, x_axis,'Percent Difference', 'PF*Sonoff vs Multimeter Current Percent Diff', 212, 'PF')
    plt.tight_layout()
    plt.savefig(f"{argv[1].split('.')[0]}_scatter.png")

if __name__ == '__main__':
    main()
"""Writes data to Excel spreadsheet

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Collects metadata and measurements and writes to Excel.
"""
import pandas as pd
import time
import os


def group_and_summarize(data_list):
    """Groups and summarizes the data
    
    Arguments:
        data_list {list} -- list of the data returned from image processing
    
    Returns:
        [tuple] -- (raw data collected from each image, grouped data based on image metadata)
    """
    raw_df = pd.DataFrame(data_list)
    grouped_df = raw_df.groupby(['Animal_id', 'Location', 'Species', 'Magnification', 'Fixed_Field']).mean().reset_index()

    # sort data sheets - if can't, not important - pass
    try:
        raw_df = raw_df.sort_values(['Animal_id', 'Location', 'Img_num'], ascending=[True, True, True])
        grouped_df = grouped_df.sort_values(['Animal_id', 'Location', 'Img_num'], ascending=[True, True, True])
    except:
        print("Raw data could not be sorted - ignoring group operation")

    # Rearrange order of columns
    raw_df = raw_df[["FileName", "Animal_id", "Location", "Img_num", "Species", "Magnification", "Fixed_Field",  "Scale(px/um)", 
                    "Image_Width(um)", "Image_Height(um)","Obj_Num", "Mean_Area(sq_um)", "Stdev_Area(sq_um)", "Mean_Dia(um)", 
                    "Mean_Per(um)", "Total_Airspace_Area(sq_um)", "Total_Tissue_Area(sq_um)", "EXP", "Lm(um)", "D0", "D1", "D2"]]
    grouped_df = grouped_df[["Animal_id", "Location", "Img_num", "Species", "Magnification", "Fixed_Field",  "Scale(px/um)", 
                    "Image_Width(um)", "Image_Height(um)","Obj_Num", "Mean_Area(sq_um)", "Stdev_Area(sq_um)", "Mean_Dia(um)", 
                    "Mean_Per(um)", "Total_Airspace_Area(sq_um)", "Total_Tissue_Area(sq_um)", "EXP", "Lm(um)", "D0", "D1", "D2"]]
        
    return raw_df, grouped_df


def write_output(data_list, output_path):
    """Writes DataFrames to Excel file
    
    Arguments:
        data_list {list} -- list of the data returned from image processing
        output_path {str} -- path to write Excel file
    """
    print(f"Writing results to {output_path}")
    print("#" * 80)
    df1, df2 = group_and_summarize(data_list)

    timestr = time.strftime("%Y%m%d-%H%M%S")

    with pd.ExcelWriter(os.path.join(output_path, "Lung_Data_{}.xlsx".format(timestr)), engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="Raw Data", index=False)
        df2.to_excel(writer, sheet_name="Grouped Averages", index=False)

        s1 = writer.sheets['Raw Data']
        s2 = writer.sheets['Grouped Averages']

        # add comments to each sheet
        s1.write_comment('A1', 'FileName of the processed image')
        s1.write_comment('B1', 'Animal ID - derived from the first field of the FileName')
        s1.write_comment('C1', 'Location - derived from the second field of the FileName')
        s1.write_comment('D1', 'Image Number - image Number derived from the third field of the FileName')
        s1.write_comment('E1', 'Species - Species label obtained from the config_file [Image_metadata]')
        s1.write_comment('F1', 'Magnification  - Magnification of the objective obtained from the config_file [Image_metadata]')
        s1.write_comment('G1', 'Fixed Field - Size of the fixed field (image) in pixels. Obtained from the config_file [Image_metadata]')
        s1.write_comment('H1', 'Scale - Scale of the image in pixels/micrometer')
        s1.write_comment('I1', 'Image Width - Width of the image in micrometers')
        s1.write_comment('J1', 'Image Height - Height of the image in micrometers')
        s1.write_comment('K1', 'Object Number - The number of unique airspaces counted in the image')
        s1.write_comment('L1', 'Mean Area - The mean area of an airspace in the image given in square micrometers')
        s1.write_comment('M1', 'Stdev Area - The standard deviation of the mean area of the airspaces in the image given in square micrometers')
        s1.write_comment('N1', 'Mean Diameter - The mean of the equivalent diameters of the airspaces in the image given in micrometers')
        s1.write_comment('O1', 'Mean Perimeter - The mean of the perimeters of the airspaces in the image given in micrometers')
        s1.write_comment('P1', 'Total Airspace Area - The total area of the airspaces in the image given in square micrometers')
        s1.write_comment('Q1', 'Total Tissue Area - The total area of the tissue in the image given in square micrometers')
        s1.write_comment('R1', 'Expansion Index (EXP) - Calculated as (Airspace_Area:Tissue_Area) * 100')
        s1.write_comment('S1', 'Mean linear Intercept (Lm) - Mean Linear Intercept estimate given in micrometers')
        s1.write_comment('T1', 'D0 Index - A weighted mean of the equivalent diameter. Measured in micrometers. Note: D0 is equivalent to Mean_Dia(um)')
        s1.write_comment('U1', 'D1 index - A weighted mean of the equivalent diameter. Measured in micrometers. D1 is a function of the mean and the variance of the airspace diameters')
        s1.write_comment('V1', 'D2 Index - A weighted mean of the equivalent diameter. Measured in micrometers. D2 is a function of the mean, variance, and skew of the airspace diameters')
        
        # on Grouped Averages Sheet
        s2.write_comment('A1', 'FileName of the processed image')
        s2.write_comment('B1', 'Animal ID - derived from the first field of the FileName')
        s2.write_comment('C1', 'Location - derived from the second field of the FileName')
        s2.write_comment('D1', 'Image Number - image Number derived from the third field of the FileName')
        s2.write_comment('E1', 'Species - Species label obtained from the config_file [Image_metadata]')
        s2.write_comment('F1', 'Magnification  - Magnification of the objective obtained from the config_file [Image_metadata]')
        s2.write_comment('G1', 'Fixed Field - Size of the fixed field (image) in pixels. Obtained from the config_file [Image_metadata]')
        s2.write_comment('H1', 'Scale - Scale of the image in pixels/micrometer')
        s2.write_comment('I1', 'Image Width - Width of the image in micrometers')
        s2.write_comment('J1', 'Image Height - Height of the image in micrometers')
        s2.write_comment('K1', 'Object Number - The number of unique airspaces counted in the image')
        s2.write_comment('L1', 'Mean Area - The mean area of an airspace in the image given in square micrometers')
        s2.write_comment('M1', 'Stdev Area - The standard deviation of the mean area of the airspaces in the image given in square micrometers')
        s2.write_comment('N1', 'Mean Diameter - The mean of the equivalent diameters of the airspaces in the image given in micrometers')
        s2.write_comment('O1', 'Mean Perimeter - The mean of the perimeters of the airspaces in the image given in micrometers')
        s2.write_comment('P1', 'Total Airspace Area - The total area of the airspaces in the image given in square micrometers')
        s2.write_comment('Q1', 'Total Tissue Area - The total area of the tissue in the image given in square micrometers')
        s2.write_comment('R1', 'Expansion Index (EXP) - Calculated as (Airspace_Area:Tissue_Area) * 100')
        s2.write_comment('S1', 'Mean linear Intercept (Lm) - Mean Linear Intercept estimate given in micrometers')
        s2.write_comment('T1', 'D0 Index - A weighted mean of the equivalent diameter. Measured in micrometers. Note: D0 is equivalent to Mean_Dia(um)')
        s2.write_comment('U1', 'D1 index - A weighted mean of the equivalent diameter. Measured in micrometers. D1 is a function of the mean and the variance of the airspace diameters')
        s2.write_comment('V1', 'D2 Index - A weighted mean of the equivalent diameter. Measured in micrometers. D2 is a function of the mean, variance, and skew of the airspace diameters')
    
        writer.save()

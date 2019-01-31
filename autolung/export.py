"""
This script attempts to group and write the data collected by the processing
to an excel file 
"""
import pandas as pd
import time
import os


def group_and_summarize(data_list):
    """Group and summarize the results DataFrame"""
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
    """Write the Dataframes to an Excel File"""
    print("Writing results to {}".format(output_path))
    print("#" * 80)
    df1, df2 = group_and_summarize(data_list)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    writer = pd.ExcelWriter(os.path.join(output_path, "Lung_Data_{}.xlsx".format(timestr)))
    df1.to_excel(writer, sheet_name="Raw Data", index=False)
    df2.to_excel(writer, sheet_name="Grouped Averages", index=False)
    writer.save()
